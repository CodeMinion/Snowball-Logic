#include <bluefruit.h>

#define STATUS_LED (19)
/* Snowball Thrusters LED Service Definitions
   Snowball Thrusters LED Service:  0x38FF
   Thrusters Pattern Char: 0x3A38
*/

// Power Reduction: https://github.com/adafruit/Adafruit_nRF52_Arduino/issues/165
// Serial seems to increase consumption by 500uA https://github.com/adafruit/Adafruit_nRF52_Arduino/issues/51#issuecomment-368289198
#define DEBUG

#ifdef DEBUG
  #define DEBUG_PRINT(x)  Serial.print(x)
  #define DEBUG_PRINTLN(x)  Serial.println(x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif


const char* DEVICENAME = "Snowball %X%X";
const char* DEVICE_MODEL = "Snowball Thrusters";
const char* DEVICE_MANUFACTURER = "Rounin Labs";

/**
   This service exposes data about the thursters patterns for Snowball.
 **/
const int UUID16_SVC_SNOWBALL_THURSTERS = 0x38FF;
const int UUID16_CHR_SNOWBALL_THURSTERS_PATTERN_MEASUREMENT = 0x3A38;

/**
 * 00 - Thursters Off
 * 01 - Thursters On
 */
volatile int thurstersValue = 0x00;

BLEService        hess = BLEService(UUID16_SVC_SNOWBALL_THURSTERS);
BLECharacteristic lsc = BLECharacteristic(UUID16_CHR_SNOWBALL_THURSTERS_PATTERN_MEASUREMENT);

BLEDis bledis;    // DIS (Device Information Service) helper class instance
BLEBas blebas;    // BAS (Battery Service) helper class instance


const int BATTERY_INFO_PIN = A7;
// Level at which to signal low battery
const int LOW_BATT = 25;
int lastBattLevel = 100;
// Interval at which the battery is reported in MS
const int BATT_REPORTING_INTERVAL = 60000;

const int iThrustersPin = A3;

/**
   Basic task informaiton
*/
static TaskHandle_t _notifyLeakValueHandle;
static TaskHandle_t _taskToNotify;

uint32_t _notifyLeakValueStackSize = 512;
void TaskNotifyLeak(void * pvParameters);


void setup()
{
  
  #ifdef DEBUG
  Serial.begin(115200);
  while ( !Serial ) delay(10);   // for nrf52840 with native usb
  #endif
  
  DEBUG_PRINTLN("Setting up Thursters");
  DEBUG_PRINTLN("-----------------------\n");

  pinMode(STATUS_LED, OUTPUT);

  // Initialise the Bluefruit module
  DEBUG_PRINTLN("Initialise the Bluefruit nRF52 module");
  Bluefruit.begin();

  // We'll control the LED so we can save some power.
  Bluefruit.autoConnLed(false);

  // Set the advertised device name (keep it short!)
  DEBUG_PRINT("Setting Device Name to ");
  uint8_t address [6];
  Bluefruit.Gap.getAddr(address);
  char nameBuff[50] = "";
  sprintf(nameBuff, DEVICENAME, address[1], address[0]);
  DEBUG_PRINTLN(nameBuff);
  Bluefruit.setName(nameBuff);

  // Set the connect/disconnect callback handlers
  Bluefruit.setConnectCallback(connect_callback);
  Bluefruit.setDisconnectCallback(disconnect_callback);

  // Configure and Start the Device Information Service
  DEBUG_PRINTLN("Configuring the Device Information Service");
  bledis.setManufacturer(DEVICE_MANUFACTURER);
  bledis.setModel(DEVICE_MODEL);
  bledis.begin();

  // Start the BLE Battery Service and set it to 100%
  DEBUG_PRINTLN("Configuring the Battery Service");
  blebas.begin();
  blebas.write(100);

  // Setup the Heart Rate Monitor service using
  // BLEService and BLECharacteristic classes
  DEBUG_PRINTLN("Configuring the Thrusters Service");
  setupThrusterService();

  // Setup the advertising packet(s)
  DEBUG_PRINTLN("Setting up the advertising payload(s)");
  startAdv();
  DEBUG_PRINTLN("\nAdvertising");

  //Setup Thursters Pin.
  setupThursters();
  
  // Setup FreeRTOS notification tasks
  DEBUG_PRINTLN("Setting up FreeRTOS notification task(s)");
  
  DEBUG_PRINTLN("\nSetup Complete!");
}

void connect_callback(uint16_t conn_handle)
{
  char central_name[32] = { 0 };
  Bluefruit.Gap.getPeerName(conn_handle, central_name, sizeof(central_name));

  DEBUG_PRINT("Connected to ");
  DEBUG_PRINTLN(central_name);
  // Disable the BT connection LED to save battery.
  digitalWrite(STATUS_LED, LOW);
}

/**
   Helper function to notify the battery level.
*/
void notifyBatteryLevel(int level)
{
  blebas.notify(level);
}

/**
   Callback invoked when a connection is dropped
   @param conn_handle connection where this event happens
   @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
   https://github.com/adafruit/Adafruit_nRF52_Arduino/blob/master/cores/nRF5/nordic/softdevice/s140_nrf52_6.1.1_API/include/ble_hci.h
*/
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  DEBUG_PRINTLN("Disconnected");

  // Consider ligthing LED when it is disconnected.
}

void cccd_callback(BLECharacteristic& chr, uint16_t cccd_value)
{
  // Display the raw request packet
  DEBUG_PRINT("CCCD Updated: ");
  //Serial.printBuffer(request->data, request->len);
  DEBUG_PRINT(cccd_value);
  DEBUG_PRINTLN("");

  // Check the characteristic this CCCD update is associated with in case
  // this handler is used for multiple CCCD records.
  if (chr.uuid == lsc.uuid)
  {
    if (chr.notifyEnabled())
    {
      DEBUG_PRINTLN("Leak Sensing Measurement 'Notify' enabled");
      // Notify current leak
    }
    else
    {
      DEBUG_PRINTLN("Leak Sensing Measurement 'Notify' disabled");
    }
  }
      
}

void thurster_write_callback(BLECharacteristic& chr, uint8_t* data, uint16_t len, uint16_t offset) 
{
  
  DEBUG_PRINTLN("Pattern Measurement: ");
  
  if(chr.uuid == lsc.uuid) 
  {
    DEBUG_PRINTLN("Thruster Pattern");
    DEBUG_PRINTLN(data[0]);

    uint8_t pattern = data[0];
    if(pattern == 0)
    {
      turnOffThrusters();
    }
    else 
    {
      turnOnThrusters();
    }
  }
}

void setupThrusterService(void)
{
  // Configure the Thrusters service
  // Supported Characteristics:
  // Name                         UUID    Requirement Properties
  // ---------------------------- ------  ----------- ----------
  // Snowball Thrusters LED Service  0x38FF  Mandatory   Read|Write
  hess.begin();

  // Note: You must call .begin() on the BLEService before calling .begin() on
  // any characteristic(s) within that service definition.. Calling .begin() on
  // a BLECharacteristic will cause it to be added to the last BLEService that
  // was 'begin()'ed!

  lsc.setProperties(CHR_PROPS_READ|CHR_PROPS_WRITE|CHR_PROPS_NOTIFY);
  // Read Permissions, Write Permission
  lsc.setPermission(SECMODE_OPEN, SECMODE_OPEN);
  lsc.setFixedLen(2);
  lsc.setWriteCallback(thurster_write_callback);
  lsc.setCccdWriteCallback(cccd_callback);  // Optionally capture CCCD updates
  lsc.setUserDescriptor("Thursters Pattern. A value of greater than 0 means thursters on.");
  lsc.begin();
  uint8_t lsdata[1] = { 0 }; // Set the characteristic to use 8-bit values, with the sensor connected and detected
  lsc.notify(lsdata, 1);     // Use .notify instead of .write!              

}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include Motion Sensor Service UUID
  Bluefruit.Advertising.addService(hess);

  // Include Name
  Bluefruit.Advertising.addName();

  /* Start Advertising
     - Enable auto advertising if disconnected
     - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
     - Timeout for fast mode is 30 seconds
     - Start(timeout) with timeout = 0 will advertise forever (until connected)

     For recommended advertising interval
     https://developer.apple.com/library/content/qa/qa1931/_index.html
  */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds
}

/**
   Setup the pin for handling the Thrusters LEDs
*/
void setupThursters()
{
  pinMode(iThrustersPin, OUTPUT);
  digitalWrite(iThrustersPin, LOW);
}

void turnOnThrusters()
{
  digitalWrite(iThrustersPin, HIGH);  
}

void turnOffThrusters()
{
  digitalWrite(iThrustersPin, LOW);  
}

void loop()
{
  if (Bluefruit.connected() )
  {
    int batteryLevel = readBatteryLevel();

    // Notify the battery level only if it has changed.
    if (batteryLevel != lastBattLevel)
    {
      notifyBatteryLevel(batteryLevel);
      lastBattLevel = batteryLevel;
    }

  }

  // Only send update every BATT_REPORTING_INTERVAL milliseconds
  delay(BATT_REPORTING_INTERVAL);

}



/**
   Reads the battery level from the feather pin.
   Note: Updated from: https://learn.adafruit.com/adafruit-feather-32u4-basic-proto/power-management
*/

/**
   Excerpt From https://github.com/adafruit/Adafruit_nRF52_Arduino/blob/master/libraries/Bluefruit52Lib/examples/Hardware/adc_vbat/adc_vbat.ino
*/
#define VBAT_PIN          (A7)
#define VBAT_MV_PER_LSB   (0.73242188F)   // 3.0V ADC range and 12-bit ADC resolution = 3000mV/4096
#define VBAT_DIVIDER      (0.71275837F)   // 2M + 0.806M voltage divider on VBAT = (2M / (0.806M + 2M))
#define VBAT_DIVIDER_COMP (1.403F)        // Compensation factor for the VBAT divider

int readVBAT(void)
{
  int raw;

  // Set the analog reference to 3.0V (default = 3.6V)
  analogReference(AR_INTERNAL_3_0);

  // Set the resolution to 12-bit (0..4095)
  analogReadResolution(12); // Can be 8, 10, 12 or 14

  // Let the ADC settle
  delay(1);

  // Get the raw 12-bit, 0..3000mV ADC value
  raw = analogRead(VBAT_PIN);

  // Set the ADC back to the default settings
  analogReference(AR_DEFAULT);
  analogReadResolution(10);

  return raw;
}

uint8_t mvToPercent(float mvolts) {
  uint8_t battery_level;

  if (mvolts >= 3000)
  {
    battery_level = 100;
  }
  else if (mvolts > 2900)
  {
    battery_level = 100 - ((3000 - mvolts) * 58) / 100;
  }
  else if (mvolts > 2740)
  {
    battery_level = 42 - ((2900 - mvolts) * 24) / 160;
  }
  else if (mvolts > 2440)
  {
    battery_level = 18 - ((2740 - mvolts) * 12) / 300;
  }
  else if (mvolts > 2100)
  {
    battery_level = 6 - ((2440 - mvolts) * 6) / 340;
  }
  else
  {
    battery_level = 0;
  }

  return battery_level;
}

int readBatteryLevel()
{
  /*
    float measuredvbat = analogRead(BATTERY_INFO_PIN);
    measuredvbat *= 2;    // we divided by 2, so multiply back
    measuredvbat *= 3.3;  // Multiply by 3.3V, our reference voltage
    measuredvbat /= 1024; // convert to voltage
    DEBUG_PRINT("VBat: " ); DEBUG_PRINTLN(measuredvbat);
    DEBUG_PRINT("CBat: " ); DEBUG_PRINTLN(map(measuredvbat, 3.0, 4.2, 0, 100));
  */
  int vbat_raw = readVBAT();

  // Convert from raw mv to percentage (based on LIPO chemistry)
  uint8_t vbat_per = mvToPercent(vbat_raw * VBAT_MV_PER_LSB);
  DEBUG_PRINT("VBat: " ); DEBUG_PRINT(vbat_per); DEBUG_PRINTLN("%");
  return vbat_per;
}
