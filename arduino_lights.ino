#include <FastLED.h>
const int led_number = 5;
const int data_pin = 6;
CRGB leds[led_number];

const int answer_hue = 200;
const int listening_hue = 180;
const int idle_hue = 0;
const int thinking_hue = 150;
const int music_hue =170;
const int music_delay = 50;



void setup() {
  // put your setup code here, to run once:
  FastLED.addLeds<WS2812B,data_pin,GRB>(leds,led_number);
  FastLED.setMaxPowerInVoltsAndMilliamps(5,400);
  Serial.begin(115200);
  FastLED.clear();
  FastLED.show();

}

void loop(){
    
  if (Serial.available() > 0){
    uint8_t bass = Serial.read();
    music(bass);
  }
  else{
    idle();
  }
// still have to write code for different scenarios



  // listening();
  // idle();
  // answer();
  // rainbow();

}



void idle(){
  for (int i=0;i<=led_number-1;i++){
    leds[i] = CHSV(idle_hue,0,0);
  }
  FastLED.show();
}

void listening(){
  for (int i= 0;i<=led_number-1;i++){
    leds[i] = CHSV(listening_hue,255,255);
    FastLED.show();
    delay(50);
  }
}

void thinking(){
  for (int i=0;i<=led_number-1;i++){
    leds[i] = CHSV(thinking_hue,255,255);
    FastLED.show();
    leds[i] = CHSV(0,0,0);
    delay(75);

  }
    delay(75);
}


void answer(){
  for (int i=0;i <=led_number-1;i++){
    leds[i] = CHSV(answer_hue,255,255);
  }
  FastLED.show();
}

void rainbow(){
  for (int i=0; i <= 255; i++){
    for (int j =0 ; j <=4; j++){
      leds[j] = CHSV(i,255,255);
    }
    FastLED.show();
    delay(50);
  }
}

void music(uint8_t bass){
  
  for (int i=0;i<=led_number-1;i++){
    leds[i] = CHSV(music_hue,255,bass);
    FastLED.show();
  }

}

