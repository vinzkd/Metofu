#include <Servo.h>
#define Lpwm_pin 5 // pin of controlling speed---- ENA of motor driver board
#define Rpwm_pin 6 // pin of controlling speed---- ENB of motor driver board
int pinLB = 2;     // pin of controlling turning---- IN1 of motor driver board
int pinLF = 4;     // pin of controlling turning---- IN2 of motor driver board
int pinRB = 7;     // pin of controlling turning---- IN3 of motor driver board
int pinRF = 8;     // pin of controlling turning---- IN4 of motor driver board
Servo myservo;
volatile int DL;
volatile int DM;
volatile int DR;
String command = "";

bool manualMode = false;


float checkdistance() {
  digitalWrite(A1, LOW);
  delayMicroseconds(2);
  digitalWrite(A1, HIGH);
  delayMicroseconds(10);
  digitalWrite(A1, LOW);
  float distance = pulseIn(A0, HIGH) / 58.00;
  delay(10);
  return distance;
}

void Detect_obstacle_distance() {
  myservo.write(160);
  for (int i = 0; i < 3; i = i + 1) {
    DL = checkdistance();
    delay(100);
  }
  myservo.write(20);
  for (int i = 0; i < 3; i = i + 1) {
    DR = checkdistance();
    delay(100);
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("Starting");
  myservo.attach(A2);
  pinMode(A1, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(pinLB, OUTPUT);    // /pin 2
  pinMode(pinLF, OUTPUT);    // pin 4
  pinMode(pinRB, OUTPUT);    // pin 7
  pinMode(pinRF, OUTPUT);    // pin 8
  pinMode(Lpwm_pin, OUTPUT); // pin 5 (PWM)
  pinMode(Rpwm_pin, OUTPUT); // pin6(PWM)
  DL = 0;
  DM = 0;
  DR = 0;
  myservo.write(90);
}


void loop() {
  Set_Speed(100);

  // // Listen to serial for joystick
  // while (Serial.available()) {
  //   char c = Serial.read();
  //   command += c;
  //   if (c == '\n') { // End of command
  //     processJoystick(command);
  //     command = ""; // Reset command string
  //   }   
  // }


 // Set up serial message receiving for Chatbot AI
 while (Serial.available()) {
   char c = Serial.read();
   if (c == '\n') { // End of command
     processCommand(command);
     command = ""; // Reset command string
   } else {
     command += c; // Append character to command string
   }
 }

  
  if (Serial.available() > 0) {
      char command = Serial.read();
      Serial.println(command);
      switch (command) {
          case 'f': // Move Forward
              advance();
              delay(2000);
              stop();
              break;
          case 'b': // Move Backward
              back();
              delay(2000);
              stop();
              break;
          case 'l': // Turn Left
              turnL();
              delay(1000);
              stop();
              break;
          case 'r': // Turn Right
              turnR();
              delay(1000);
              stop();
              break;
          case 's': // Stop
              stop();
              break;
          case 'h':
              shakehead();
              break;
          default:
              break;
      }
  }
}


// Robot movement functions
void Set_Speed(unsigned char pwm) // function of setting speed
{
  analogWrite(Lpwm_pin, pwm);
  analogWrite(Rpwm_pin, pwm);
}
void advance() //  going forward
{
  digitalWrite(pinRB, LOW); // making motor move towards right rear
  digitalWrite(pinRF, HIGH);
  digitalWrite(pinLB, LOW); // making motor move towards left rear
  digitalWrite(pinLF, HIGH);
}
void turnR() // turning right(dual wheel)
{
  digitalWrite(pinRB, LOW); // making motor move towards right rear
  digitalWrite(pinRF, HIGH);
  digitalWrite(pinLB, HIGH);
  digitalWrite(pinLF, LOW); // making motor move towards left front
}
void turnL() // turning left(dual wheel)
{
  digitalWrite(pinRB, HIGH);
  digitalWrite(pinRF, LOW); // making motor move towards right front
  digitalWrite(pinLB, LOW); // making motor move towards left rear
  digitalWrite(pinLF, HIGH);
}
void stop() // stop
{
  digitalWrite(pinRB, HIGH);
  digitalWrite(pinRF, HIGH);
  digitalWrite(pinLB, HIGH);
  digitalWrite(pinLF, HIGH);
}
void back() // back up
{
  digitalWrite(pinRB, HIGH); // making motor move towards right rear
  digitalWrite(pinRF, LOW);
  digitalWrite(pinLB, HIGH); // making motor move towards left rear
  digitalWrite(pinLF, LOW);
}
void shakehead()
{
    myservo.write(160);
    delay(100);
    myservo.write(20);
    delay(100);
    myservo.write(85);
    myservo.write(160);
    delay(100);
    myservo.write(20);
    delay(100);
    myservo.write(85);
    myservo.write(160);
    delay(100);
    myservo.write(20);
    delay(100);
    myservo.write(85);
    myservo.write(160);
    delay(100);
    myservo.write(20);
    delay(100);
    myservo.write(85);
}



// Process serial messages
void processCommand(String cmd) {
  cmd.trim(); // Remove whitespace

  //  ChatGPT commands  //
       if (cmd == "move_forward") 
  { 
    advance();
    delay(2000);
    stop();
  } 
  else if (cmd == "move_backward") {
    back();
    delay(2000);
    stop();
  } 
  else if (cmd == "turn_left") {
    turnL();
    delay(1000);
    stop();
  } 
  else if (cmd == "turn_right") {
    turnR();
    delay(1000);
    stop();
  } 
  else if (cmd == "shake_head") {
    shakehead();
  } 

  //  Joystick commands  //
  else if (cmd == "joystick_move_forward") { 
    while (cmd == "joystick_move_forward") {
      advance();
    }
    stop();
  } 
  else if (cmd == "joystick_move_backward") { 
    while (cmd == "joystick_move_backward") {
      back();
    }
    stop();
  } 
  else if (cmd == "joystick_turn_left") { 
    while (cmd == "joystick_turn_left") {
      turnL();
    }
    stop();
  }
  else if (cmd == "joystick_turn_right") { 
    while (cmd == "joystick_turn_right") {
      turnR();
    }
    stop();
  }
  else if (cmd == "joystick_shake_head") {
    shakehead();
  }
  else {
    Serial.println("Invalid Command");
  }
}


void processJoystick(String cmd) {
  // Example command: "1.00:0.80:1.00"
  
  cmd.trim();  // Remove whitespace
  
  int colon1 = cmd.indexOf(':');
  int colon2 = cmd.indexOf(':', colon1 + 1);

  float linearX = cmd.substring(0, colon1).toFloat();
  float angularZ = cmd.substring(colon1 + 1, colon2).toFloat();
  float dpad_H = cmd.substring(colon2 + 1).toFloat();
  
  int headturn_speed = 4;
  float linearX_deadzone = 0.40;
  float angularZ_deadzone = 0.40;

  // Turn Head
  if (dpad_H != 0) {
    int position = myservo.read();
    position = position + (headturn_speed * dpad_H);
    myservo.write(position);
  }
 
  if (linearX > 0 + linearX_deadzone) {
    advance();
  }
  else if (linearX < 0 - linearX_deadzone) {
    back();
  }
  else if (angularZ > 0 + angularZ_deadzone) {
    turnL();
  }
  else if (angularZ < 0 - angularZ_deadzone) {
    turnR();
  }
  else {
    stop();
  }
  
  
  // if (directive == "joystick_turn_head") { 
  //   int position = myservo.read();
  //   position = position + (scale * axisValue);
  //   myservo.write(position);
  // }
  //
  // else if (directive == "joystick_move") {
  //   if (axisValue > 0 + leftX_deadzone) {
  //     advance();
  //   }
  //   else if (axisValue < 0 - leftX_deadzone) {
  //     back();
  //   }
  //   else {
  //     stop();
  //   }
  // }
  //
  // else if (directive == "joystick_turn") {
  //   if (axisValue > 0 + rightZ_deadzone) {
  //     turnL();
  //   }
  //   else if (axisValue < 0 - rightZ_deadzone) {
  //     turnR();
  //   }
  //   else {
  //     stop();
  //   }
  // }
}
