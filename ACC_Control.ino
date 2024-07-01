
#include <Servo.h>
#include <TimerOne.h>
double T, encoder, output, speed;
float distance;
Servo servo;
#define encA 2
#define encB 4
#define IN1 10
#define IN2 11
#define ENA 3
#define dwheel 65
#define pi 3.142

void setup() {
  T = 0.5;
  output = 0; 
  Serial.begin(9600);
  servo.attach(9);
  pinMode(encA, INPUT_PULLUP);
  pinMode(encB, INPUT_PULLUP);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  attachInterrupt(0, count, RISING);
  Timer1.initialize(100000); //=10^6*T
  Timer1.attachInterrupt(control);
}

void motor_Phanh(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 120);
}
void motor_Dung() {
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
}
void motor_Tien(int analog) { 
	analog = constrain(analog, 0, 255);//đảm báo giá trị nằm trong một khoảng từ 0 - MAX_SPEED
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, HIGH);
  analogWrite(ENA, analog);
}

void count() {
  if(digitalRead(encA) == 1)
    encoder++;
  else
    encoder--;
}

void control() {
    speed = 3.6*pi*dwheel*32*encoder/(21*170*T); 
    Serial.println(speed);
    encoder = 0;
  if (Serial.available()>0){
    String data = Serial.readStringUntil('\n');  // nhan du lieu khoang cach
    float distance = data.toFloat();
    Serial.println(distance);
      if (distance <= 65){
           motor_Phanh();// phanh
           servo.write(15);
      }
      else {
        if (distance < 75){
        output = output - 20 ;   // giảm tốc để khoảng cách đưa về 80 cm
        }
        else {
          if (distance <= 78){
          output = output - 10; // giữ nguyên tốc độ để duy trì khoảng cách
          }
          else {
            if (distance <= 82){
            output = output + 0;  // tăng tốc để khoảng cách đưa về 80 cm
            }
            else {
              if (speed = 25){
                output = output + 0;
              }
              else
                output = output + 10;  // tăng tốc để khoảng cách đưa về 80 cm
          }
        }
      }
  
           if (output > 150) {
    output = 150;
  }
    if (output < 0) {
    output = 0;
    }
  }
  motor_Tien(output);
  servo.write(0);
 }
void loop() {
  control();
  
 }
