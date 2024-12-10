import pygame
import threading
import asyncio
import datetime
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import random

from spade import run

from spade import run  # Ensure SPADE agents run in the same program
from smartRoom import (
    TemperatureSensorAgent, HumiditySensorAgent, LightSensorAgent,
    ACAgent, FanAgent, WindowsAgent, BulbAgent, ControllerAgent,
    FuzzyLogic, temp_agent_name, temp_agent_password,
    hum_agent_name, hum_agent_password, light_agent_name, light_agent_password,
    ac_agent_name, ac_agent_password, fan_agent_name, fan_agent_password,
    win_agent_name, win_agent_password, bulb_agent_name, bulb_agent_password,
    controller_agent_name, controller_agent_password
)

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Room Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Global Variables for Sliders
temp = 25  # Default temperature value
humidity = 50  # Default humidity value
light= 500  # Default light value
outside_brightness = 600
agents_started=False

# Fonts
FONT = pygame.font.Font(None, 24)
LARGE_FONT = pygame.font.Font(None, 36)

# Slider Dimensions
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 10

# Sliders
temp_slider_rect = pygame.Rect(1050, 60, SLIDER_WIDTH, SLIDER_HEIGHT)
humidity_slider_rect = pygame.Rect(1050, 140, SLIDER_WIDTH, SLIDER_HEIGHT)
light_slider_rect = pygame.Rect(1050, 220, SLIDER_WIDTH, SLIDER_HEIGHT)
outside_brightness_slider_rect = pygame.Rect(1050, 300, SLIDER_WIDTH, SLIDER_HEIGHT)

# Load Images
fan_img = pygame.image.load("fan_off.jpg")
fan_active_img = pygame.image.load("fan_on.jpg")
ac_img = pygame.image.load("ac_off.jpg")
ac_active_img = pygame.image.load("ac_on.png")
window_img = pygame.image.load("window_closed.jpg")
window_active_img = pygame.image.load("window_open.jpeg")
bulb_img = pygame.image.load("bulb_off.jpg")
bulb_active_img = pygame.image.load("bulb_on.jpg")

# Scale Images
fan_img = pygame.transform.scale(fan_img, (100, 100))
fan_active_img = pygame.transform.scale(fan_active_img, (100, 100))
ac_img = pygame.transform.scale(ac_img, (100, 100))
ac_active_img = pygame.transform.scale(ac_active_img, (100, 100))
window_img = pygame.transform.scale(window_img, (100, 100))
window_active_img = pygame.transform.scale(window_active_img, (100, 100))
bulb_img = pygame.transform.scale(bulb_img, (100, 100))
bulb_active_img = pygame.transform.scale(bulb_active_img, (100, 100))

# Positions
fan_pos = (50, 50)
ac_pos = (50, 200)
window_pos = (50, 350)
bulb_pos = (50, 500)

# State Variables (updated based on agent decisions)
fan_active = False
ac_active = False
window_open = False
bulb_active = False

# Start Button Properties
button_rect = pygame.Rect(1100, 400, 150, 50)  # Button dimensions and position
button_color = BLUE
button_text = "Start Agents"

ac_power = None
fan_power = None
brightness = None


restart_button_rect = pygame.Rect(1050, 600, 150, 50)

# Message log
messages = []

current_slider = None 
agents_task = None


temp_agent_active = True
hum_agent_active = True
light_agent_active = True
ac_agent_active = True
fan_agent_active = True
win_agent_active = True
bulb_agent_active = True
controller_agent_active = True

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve the agentName1 value
temp_agent_name = os.getenv('agentName1')
temp_agent_password = os.getenv('agentPassword1')
hum_agent_name = os.getenv('agentName2')
hum_agent_password = os.getenv('agentPassword2')
light_agent_name = os.getenv('agentName3')
light_agent_password = os.getenv('agentPassword3')
ac_agent_name = os.getenv('agentName4')
ac_agent_password = os.getenv('agentPassword4')
fan_agent_name = os.getenv('agentName5')
fan_agent_password = os.getenv('agentPassword5')
win_agent_name = os.getenv('agentName6')
win_agent_password = os.getenv('agentPassword6')
bulb_agent_name = os.getenv('agentName7')
bulb_agent_password = os.getenv('agentPassword7')
controller_agent_name = os.getenv('agentName8')
controller_agent_password = os.getenv('agentPassword8')

main_agents_skip_time = 650

finish_agents_count = 0


# Define Agents
class TemperatureSensorAgent(Agent):
    
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg
        
    class SenseTemperature(PeriodicBehaviour):
        async def run(self):
            global fan_active, ac_active, window_open, bulb_active, messages, temp, temp_agent_active
            
             # Simulated temperature
            print(f"\n\n\n[TemperatureSensorAgent] Sensed temperature: {temp}°C ")
            messages.append(f"[TemperatureSensorAgent] Sensed temperature: {temp}°C ")
            await self.send( self.agent.send_message(ac_agent_name, f"temperature:{temp}"))
            print(f"\n Temperature agent ---> AC agent : temperature:{temp}")
            messages.append(f"Temperature agent ---> AC agent : temperature:{temp}")
            await self.send( self.agent.send_message(win_agent_name, f"temperature:{temp}"))
            print(f"\n Temperature agent ---> windows agent : temperature:{temp}")
            messages.append(f"Temperature agent ---> windows agent : temperature:{temp}")
            await self.send( self.agent.send_message(fan_agent_name, f"temperature:{temp}"))
            print(f"\n Temperature agent ---> Fan agent : temperature:{temp}")
            messages.append(f"Temperature agent ---> Fan agent : temperature:{temp}")
            
            temp_agent_active = False
            while not temp_agent_active:
                await asyncio.sleep(1)
            
            await asyncio.sleep(5)
            #await self.agent.stop()
            #await asyncio.sleep(main_agents_skip_time+5)

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=6)
        b = self.SenseTemperature(period=2, start_at=start_at)
        self.add_behaviour(b)
        


class HumiditySensorAgent(Agent):
    
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg
        
    class SenseHumidity(PeriodicBehaviour):
        async def run(self):
            global fan_active, ac_active, window_open, bulb_active, messages, humidity, hum_agent_active
            
            print(f"\n\n\n[HumiditySensorAgent] Sensed humidity: {humidity}% ")
            messages.append(f"[HumiditySensorAgent] Sensed humidity: {humidity}% ")
            await self.send( self.agent.send_message(ac_agent_name, f"humidity:{humidity}"))
            print(f"\n Humidity agent ---> AC agent : humidity:{humidity}")
            messages.append(f"\n Humidity agent ---> AC agent : humidity:{humidity}")
            await self.send( self.agent.send_message(win_agent_name, f"humidity:{humidity}"))
            print(f"\n Humidity agent ---> Windows agent : humidity:{humidity}")
            messages.append(f"Humidity agent ---> Windows agent : humidity:{humidity}")
            await self.send( self.agent.send_message(fan_agent_name, f"humidity:{humidity}"))
            print(f"\n Humidity agent ---> Fan agent : humidity:{humidity}")
            messages.append(f"Humidity agent ---> Fan agent : humidity:{humidity}")
            
            hum_agent_active = False
            while not hum_agent_active:
                await asyncio.sleep(1)
            
            await asyncio.sleep(5)
            
            #await self.agent.stop()
            #await asyncio.sleep(main_agents_skip_time + 5)

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=6)
        b = self.SenseHumidity(period=2, start_at=start_at)
        self.add_behaviour(b)


class LightSensorAgent(Agent):
    
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg
    
    class SenseLight(PeriodicBehaviour):
        async def run(self):
            global fan_active, ac_active, window_open, bulb_active, messages, light_agent_active
            
            #light = random.randint(100, 800)  # Simulated light
            print(f"\n\n\n[LightSensorAgent] Sensed light: {light} lux ")
            messages.append(f"[LightSensorAgent] Sensed light: {light} lux ")
            await self.send(self.agent.send_message(win_agent_name, f"brightness:{light}"))
            print(f"\n Light Sensor agent ---> Windows agent : brightness:{light}")
            messages.append(f"Light Sensor agent ---> Windows agent : brightness:{light}")
            await self.send(self.agent.send_message(bulb_agent_name, f"brightness:{light}"))
            print(f"\n Light Sensor agent ---> Bulb agent : brightness:{light}")
            messages.append(f"Light Sensor agent ---> Bulb agent : brightness:{light}")
            
            light_agent_active = False
            while not light_agent_active:
                await asyncio.sleep(1)
            
            await asyncio.sleep(5)
            
            # await self.agent.stop()
            # await asyncio.sleep(main_agents_skip_time+5)

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=6)
        b = self.SenseLight(period=2, start_at=start_at)
        self.add_behaviour(b)




class FuzzyLogic:
    def __init__(self):
        # Temperature, Humidity, and Brightness fuzzy variables
        self.temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
        self.humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
        self.brightness = ctrl.Antecedent(np.arange(0, 1001, 1), 'brightness')
        self.outside_brightness = ctrl.Antecedent(np.arange(0, 1001, 1), 'outside_brightness')

        # Membership functions for inputs
        self.temperature['low'] = fuzz.trapmf(self.temperature.universe, [0, 0, 15, 25])
        self.temperature['medium'] = fuzz.trimf(self.temperature.universe, [15, 25, 35])
        self.temperature['high'] = fuzz.trapmf(self.temperature.universe, [30, 40, 50, 50])


        self.humidity['low'] = fuzz.trapmf(self.humidity.universe, [0, 0, 30, 50])
        self.humidity['medium'] = fuzz.trimf(self.humidity.universe, [40, 50, 60])
        self.humidity['high'] = fuzz.trapmf(self.humidity.universe, [50, 70, 100, 100])

        self.brightness['low'] = fuzz.trapmf(self.brightness.universe, [0, 0, 200, 400])
        self.brightness['medium'] = fuzz.trimf(self.brightness.universe, [300, 500, 700])
        self.brightness['high'] = fuzz.trapmf(self.brightness.universe, [600, 800, 1000, 1000])
        
        self.outside_brightness['low'] = fuzz.trapmf(self.outside_brightness.universe, [0, 0, 200, 400])
        self.outside_brightness['medium'] = fuzz.trimf(self.outside_brightness.universe, [300, 500, 700])
        self.outside_brightness['high'] = fuzz.trapmf(self.outside_brightness.universe, [600, 800, 1000, 1000])

        
        self.window_decision = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'window_decision')
        self.fan_power = ctrl.Consequent(np.arange(0, 101, 1), 'fan_power')
        self.ac_power = ctrl.Consequent(np.arange(0, 101, 1), 'ac_power')
        
        # Adjusted membership functions
        self.fan_power['low'] = fuzz.trapmf(self.fan_power.universe, [0, 0, 20, 40])  # Reduced range for low
        self.fan_power['medium'] = fuzz.trimf(self.fan_power.universe, [30, 50, 70])  # Shifted to higher values
        self.fan_power['high'] = fuzz.trapmf(self.fan_power.universe, [60, 80, 100, 100])  # Higher dominance for high

        self.ac_power['low'] = fuzz.trapmf(self.ac_power.universe, [0, 0, 30, 50])  # AC retains more power for low
        self.ac_power['medium'] = fuzz.trapmf(self.ac_power.universe, [40, 50, 60, 70])  # Balanced range
        self.ac_power['high'] = fuzz.trapmf(self.ac_power.universe, [50, 70, 90, 100])  # Slightly less dominant at high

        
        self.window_decision['close'] = fuzz.trimf(self.window_decision.universe, [0, 0, 1])
        self.window_decision['open'] = fuzz.trimf(self.window_decision.universe, [0, 1, 1])



        # Define fuzzy rules
        self.ac_rules = [
            ctrl.Rule(self.temperature['high'] & self.humidity['high'], 
                    self.ac_power['high']),  # High AC power for heavy duty
            ctrl.Rule(self.temperature['medium'] & self.humidity['medium'], 
                    self.ac_power['medium']),
            ctrl.Rule(self.temperature['low'] & self.humidity['low'], 
                    self.ac_power['low']),  # Low AC power for light duty
            ctrl.Rule(self.temperature['low'] & (self.humidity['medium'] | self.humidity['high']), 
                    self.ac_power['low']),  # AC stays low for low temp
            ctrl.Rule(self.temperature['medium'] & (self.humidity['low'] | self.humidity['high']), 
                    self.ac_power['medium']),
            ctrl.Rule(self.temperature['high'] | self.humidity['low'], 
                    self.ac_power['medium']),  # Slightly reduce AC for low humidity
        ]

        # Adjusted Fan rules
        self.fan_rules = [
            ctrl.Rule(self.temperature['high'] & self.humidity['high'], 
                    self.fan_power['high']),  # High fan power for heavy duty
            ctrl.Rule(self.temperature['medium'] & self.humidity['medium'], 
                    self.fan_power['medium']),
            ctrl.Rule(self.temperature['low'] & self.humidity['low'], 
                    self.fan_power['low']),  # Low fan power for light duty
            ctrl.Rule(self.temperature['low'] & (self.humidity['medium'] | self.humidity['high']), 
                    self.fan_power['medium']),  # Fan slightly higher for low temp
            ctrl.Rule(self.temperature['medium'] & (self.humidity['low'] | self.humidity['high']), 
                    self.fan_power['medium']),
            ctrl.Rule(self.temperature['high'] | self.humidity['low'], 
                    self.fan_power['high']),  # Fan compensates at high temp
        ]

        


        
        self.win_rules = [
            # If inside is dim, temperature is high, and humidity is high, and it's bright outside, close the window
            ctrl.Rule(self.brightness['low'] & self.temperature['high'] & self.humidity['high'] & self.outside_brightness['high'], 
                    self.window_decision['close']),
            
            # If inside brightness and outside brightness are medium, and temperature and humidity are medium, open the window
            ctrl.Rule(self.brightness['medium'] & self.outside_brightness['medium'] & self.temperature['medium'] & self.humidity['medium'], 
                    self.window_decision['open']),
            
            # If inside is very bright, or humidity is very low, keep the window closed
            ctrl.Rule(self.brightness['high'] | self.humidity['low'], 
                    self.window_decision['close']),
            
            # If inside brightness is low and humidity is medium, open the window (for balance)
            ctrl.Rule(self.brightness['low'] & self.humidity['medium'], 
                    self.window_decision['open']),
            
            # If it's neither dim, cold, nor dry inside, close the window
            ctrl.Rule(self.brightness['low'] & self.temperature['low'] & self.humidity['low'], 
                    self.window_decision['close']),
            
            # If the temperature inside is low but it's bright outside, and the humidity is medium, open the window
            ctrl.Rule(self.brightness['low'] & self.outside_brightness['high'] & self.humidity['medium'], 
                    self.window_decision['open']),
            
            # If it's dark inside, temperature is medium, and humidity is high, open the window for ventilation
            ctrl.Rule(self.brightness['low'] & self.temperature['medium'] & self.humidity['high'], 
                    self.window_decision['open']),
            
            # If outside brightness is low and inside humidity is high, close the window to avoid dampness
            ctrl.Rule(self.outside_brightness['low'] & self.humidity['high'], 
                    self.window_decision['close']),
            
            # If temperature inside is high, and outside is bright, but humidity inside is low, close the window
            ctrl.Rule(self.temperature['high'] & self.outside_brightness['high'] & self.humidity['low'], 
                    self.window_decision['close']),
            
            # Catch-all: If conditions do not strongly favor ventilation, close the window
            ctrl.Rule(self.brightness['high'] & self.outside_brightness['high'] & self.temperature['high'] & self.humidity['high'], 
                    self.window_decision['close']),
        ]


        self.ac_control = ctrl.ControlSystem(self.ac_rules)
        self.ac_simulation = ctrl.ControlSystemSimulation(self.ac_control)
        
        self.fan_control = ctrl.ControlSystem(self.fan_rules)
        self.fan_simulation = ctrl.ControlSystemSimulation(self.fan_control)
        
        self.window_control = ctrl.ControlSystem(self.win_rules)
        self.window_simulation = ctrl.ControlSystemSimulation(self.window_control)



             
    def compute_ac(self, temp, humidity):
        try:
            self.ac_simulation.input['temperature'] = temp
            self.ac_simulation.input['humidity'] = humidity
            self.ac_simulation.compute()
            return  self.ac_simulation.output['ac_power']
        except Exception as e:
            print(f"Error computing A/C output: {e}")
            return None, None  # Or return default values
    
    
    def compute_fan(self, temp, humidity):
        try:
            self.fan_simulation.input['temperature'] = temp
            self.fan_simulation.input['humidity'] = humidity
            self.fan_simulation.compute()
            return  self.fan_simulation.output['fan_power']
        except Exception as e:
            print(f"Error computing A/C output: {e}")
            return None, None  # Or return default values
    
    
    def compute_window(self, brightness, temp, humidity,outside_brightness):
        try:
            self.window_simulation.input['brightness'] = brightness
            self.window_simulation.input['temperature'] = temp
            self.window_simulation.input['humidity'] = humidity
            self.window_simulation.input['outside_brightness'] = outside_brightness
            self.window_simulation.compute()
            return self.window_simulation.output['window_decision']
        except Exception as e:
            print(f"Error computing window output: {e}")
            return None, None  # Or return default values




class WindowsAgent(Agent):
    def __init__(self, jid, password, fuzzy_logic):
        super().__init__(jid, password)
        self.fuzzy_logic = fuzzy_logic
        self.brightness = None
        self.temperature = None
        self.humidity = None
        
    def init(self):
        self.brightness = None
        self.temperature = None
        self.humidity = None
    
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg
        

    # Method to handle incoming messages
    def receive_message(self, msg): 
        if msg is not None:
            if msg.body.startswith("brightness:"):
                self.brightness = int(msg.body.split(":")[1])
            elif msg.body.startswith("temperature:"):
                self.temperature = int(msg.body.split(":")[1])
            elif msg.body.startswith("humidity:"):
                self.humidity = int(msg.body.split(":")[1])
            #print(f"[WindowsAgent] Received - Brightness: {self.brightness}, Temperature: {self.temperature}, Humidity: {self.humidity}")
    
    # Cyclic behaviour to manage window decision based on the received values
    class ManageWindows(PeriodicBehaviour):
        async def run(self):
            global fan_active, ac_active, window_open, bulb_active, messages, outside_brightness, finish_agents_count, win_agent_active
            
            # Call receive_message to catch incoming sensor data
            self.agent.receive_message(await self.receive(timeout=10))
            while self.agent.brightness is None or self.agent.temperature is None or self.agent.humidity is None:
                await asyncio.sleep(2)
                self.agent.receive_message(await self.receive(timeout=10))

            
            # Ensure that all necessary values are received
            if self.agent.brightness is not None and self.agent.temperature is not None and self.agent.humidity is not None:
                # Calculate decision and importance
                decision = self.agent.fuzzy_logic.compute_window(self.agent.brightness, self.agent.temperature, self.agent.humidity, outside_brightness)
                
                if not isinstance(decision, float):
                    decision = 0.511
                    
                decision = round(decision, 2)
                
                print(f"\n\n[WindowsAgent] Received :: Brightness = {self.agent.brightness}, Temp = {self.agent.temperature}, Humidity: {self.agent.humidity}")
                print(f"\n[WindowsAgent] concluded :: Decision = {decision}")
                
                messages.append(f"[WindowsAgent] Received :: Brightness = {self.agent.brightness}, Temp = {self.agent.temperature}, Humidity: {self.agent.humidity}")
                messages.append(f"[WindowsAgent] concluded :: Decision = {decision}")
               
                
                # send the decision value to controller agent            
                await self.send(self.agent.send_message(controller_agent_name, f"win_decision:{decision}"))
                print(f"\n Windows agent ---> Control agent : win_decision:{decision}")
                
                messages.append(f"Windows agent ---> Control agent : win_decision:{decision}")
                
                await asyncio.sleep(2)
                   
                # receive the strategy from the controller agent 
                strategy_msg = await self.receive(timeout=10)
                while strategy_msg is None or not strategy_msg.body.startswith("strategy:"):
                    strategy_msg = await self.receive(timeout=10)
                    
                strategy =  strategy_msg.body.split(":")[1]
                print(f"\n[WindowsAgent] Received strategy: {strategy} ")
                
                if strategy == "WF" or strategy == "W" or strategy == "WB" or strategy == "WFB":
                    window_open = True
                    
                    print("[WindowsAgent] The Window will be opened \n") 
                    messages.append("[WindowsAgent] The Window will be opened ")
                else:
                    window_open = False
                    print("[WindowsAgent] The Window will be closed \n")
                    messages.append("[WindowsAgent] The Window will be closed")
                
                finish_agents_count += 1
                
                win_agent_active = False
                while not win_agent_active:
                    await asyncio.sleep(1)
                    
                # await self.agent.stop()
                # await asyncio.sleep(main_agents_skip_time)
                self.agent.init()
                
                

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        b = self.ManageWindows(period=10, start_at=start_at)
        self.add_behaviour(b)
        
        

class ACAgent(Agent):
    def __init__(self, jid, password, fuzzy_logic):
        super().__init__(jid, password)
        self.fuzzy_logic = fuzzy_logic
        self.temperature = None
        self.humidity = None
        
    def init(self):
        self.temperature = None
        self.humidity = None
        
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg

    # Method to handle incoming messages
    async def receive_message(self, msg):
        if msg:
            if msg.body.startswith("temperature:"):
                self.temperature = int(msg.body.split(":")[1])
            elif msg.body.startswith("humidity:"):
                self.humidity = int(msg.body.split(":")[1])
       
            #print(f"\n\n[ACAgent] Received -  Temperature: {self.temperature}, Humidity: {self.humidity}")

    class ManageAC(PeriodicBehaviour):
        async def run(self):
                global fan_active, ac_active, window_open, bulb_active, messages, finish_agents_count, ac_power, ac_agent_active
                
                await self.agent.receive_message(await self.receive(timeout=10) )

                while self.agent.temperature is None or self.agent.humidity is None:
                    #await asyncio.sleep(2)
                    await self.agent.receive_message(await self.receive(timeout=10))
                    
                if self.agent.temperature is not None and self.agent.humidity is not None:
                    # Calculate decision and importance
                    ac_power = self.agent.fuzzy_logic.compute_ac(self.agent.temperature, self.agent.humidity)
                    
                    if not isinstance(ac_power, float):
                        ac_power = 42.33
                        
                    ac_power = round(ac_power, 2)
                    
                    print(f"[ACAgent] Temp: {self.agent.temperature}, Humidity: {self.agent.humidity}")
                    messages.append(f"[ACAgent] Temp: {self.agent.temperature}, Humidity: {self.agent.humidity}")
                    
                    print(f"[ACAgent] Calculated  ac_power: {ac_power}")
                    messages.append(f"[ACAgent] Calculated  ac_power: {ac_power}")

                    await self.send(self.agent.send_message(controller_agent_name, f"ac_power:{ac_power}"))
                    
                    print(f"AC agent ---> Control agent : ac_power:{ac_power}")
                    messages.append(f"AC agent ---> Control agent : ac_power:{ac_power}")
                    
                    await asyncio.sleep(2)
                    
                    strategy_msg = await self.receive(timeout=10)
                    while strategy_msg is None or not strategy_msg.body.startswith("strategy:"):
                        strategy_msg = await self.receive(timeout=10)
                        
                    strategy =  strategy_msg.body.split(":")[1]
                    print(f"\n[ACAgent] Received strategy: {strategy}")
                    
                    if strategy == "BA" or strategy == "A":
                        ac_active = True
                        print(f"[ACAgent] The AC will be turned on with {ac_power} power")
                        messages.append(f"[ACAgent] The AC will be turned on with {ac_power} power")
                    else:
                        ac_active = False
                        print("[ACAgent] The AC will be turned off")
                        messages.append("[ACAgent] The AC will be turned off")
                        
                    finish_agents_count+=1
                    
                    ac_agent_active = False
                    while not ac_agent_active:
                        await asyncio.sleep(1)
                    
                    # self.agent.init()
                    # await self.agent.stop()
                    # await asyncio.sleep(main_agents_skip_time)
                    
                    
                    
                    
                        
                # Compare importance values
                # if ac_importance > self.agent.win_importance:
                #     response = Message(to=msg.sender)
                #     response.body = "A/C"
                # else:
                #     response = Message(to=msg.sender)
                #     response.body = "windows"
                # await self.send(response)

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        b = self.ManageAC(period=2, start_at=start_at)
        self.add_behaviour(b)


class FanAgent(Agent):
    def __init__(self, jid, password, fuzzy_logic):
        super().__init__(jid, password)
        self.fuzzy_logic = fuzzy_logic
        self.temperature = None
        self.humidity = None
    
    def init(self):
        self.temperature = None
        self.humidity = None
                
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg

    # Method to handle incoming messages
    async def receive_message(self, msg):
        if msg:
            if msg.body.startswith("temperature:"):
                self.temperature = int(msg.body.split(":")[1])
            elif msg.body.startswith("humidity:"):
                self.humidity = int(msg.body.split(":")[1])
     
            #print(f"\n\n[FanAgent] Received -  Temperature: {self.temperature}, Humidity: {self.humidity}")

    class ManageFan(PeriodicBehaviour):
        async def run(self):
                
                global fan_active, messages, fan_power, finish_agents_count, fan_agent_active
                
                await self.agent.receive_message(await self.receive(timeout=10) )

                if self.agent.temperature is not None and self.agent.humidity is not None:
                    # Calculate decision and importance
                    fan_power = self.agent.fuzzy_logic.compute_fan(self.agent.temperature, self.agent.humidity)
                    
                    if not isinstance(fan_power, float):
                        fan_power = 40.223
                        
                    fan_power = round(fan_power, 2)
                    
                    print(f"[FanAgent] Temp: {self.agent.temperature}, Humidity: {self.agent.humidity}")
                    messages.append(f"[FanAgent] Temp: {self.agent.temperature}, Humidity: {self.agent.humidity}")
                    
                    print(f"[FanAgent] Calculated  fan_power: {fan_power}")
                    messages.append(f"[FanAgent] Calculated  fan_power: {fan_power}")

                    # sending the fan_power to controller agent
                    await self.send(self.agent.send_message(controller_agent_name, f"fan_power:{fan_power}"))
                    print(f"Fan agent ---> Control agent : fan_power:{fan_power}")
                    messages.append(f"Fan agent ---> Control agent : fan_power:{fan_power}")
                    
                    await asyncio.sleep(2)
                    
                    strategy_msg = await self.receive(timeout=10)
                    while strategy_msg is None or not strategy_msg.body.startswith("strategy:"):
                        strategy_msg = await self.receive(timeout=10)
                        
                    strategy =  strategy_msg.body.split(":")[1]
                    print(f"[FanAgent] Received strategy: {strategy}")
                    messages.append(f"[FanAgent] Received strategy: {strategy}")
                    
                    if strategy == "WF" or strategy == "WFB":
                        fan_active = True
                        print(f"[FanAgent] The fan will be turned on with {fan_power*0.8} power")
                        messages.append(f"[FanAgent] The fan will be turned on with {fan_power*0.8} power")
                    elif strategy == "BF" or strategy == "F":
                        fan_active = True
                        print(f"[FanAgent] The fan will be turned on with {fan_power} power")
                        messages.append(f"[FanAgent] The fan will be turned on with {fan_power} power")
                    else:
                        fan_active = False
                        print("[FanAgent] The fan will be turned off")
                        messages.append("[FanAgent] The fan will be turned off")
                    
                    finish_agents_count += 1
                    
                    fan_agent_active = False
                    while not fan_agent_active:
                        await asyncio.sleep(1)
                    
                    # await self.agent.stop()
                    # self.agent.init()
                    # await asyncio.sleep(main_agents_skip_time)
                    
                    
                    
                    
                    
                # Compare importance values
                # if ac_importance > self.agent.win_importance:
                #     response = Message(to=msg.sender)
                #     response.body = "A/C"
                # else:
                #     response = Message(to=msg.sender)
                #     response.body = "windows"
                # await self.send(response)

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        b = self.ManageFan(period=3, start_at=start_at)
        self.add_behaviour(b)


class BulbAgent(Agent):
    def __init__(self, jid, password, fuzzy_logic):
        super().__init__(jid, password)
        self.fuzzy_logic = fuzzy_logic
        self.brightness = None
        
    def init(self):
        self.brightness = None
    
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg
        

    # Method to handle incoming messages
    def receive_message(self, msg): 
        if msg is not None:
            if msg.body.startswith("brightness:"):
                self.brightness = int(msg.body.split(":")[1])
           

            #print(f"[BulbAgent] Received - Brightness: {self.brightness}")
    
    # Cyclic behaviour to manage window decision based on the received values
    class ManageBulb(PeriodicBehaviour):
        async def run(self):
            
            global bulb_active, messages, brightness, finish_agents_count, brightness, bulb_agent_active
            
            # Call receive_message to catch incoming sensor data
            self.agent.receive_message(await self.receive(timeout=10))

            if self.agent.brightness is not None: 
                # Calculate decision and importance
                bulb_brightness = 700 - self.agent.brightness
                
                bulb_brightness = round(bulb_brightness, 2)
                
                print(f"\n[BulbAgent] Received -> Brightness: {self.agent.brightness}")
                messages.append(f"[BulbAgent] Received -> Brightness: {self.agent.brightness}")
                
                # sending the fan_power to controller agent
                await self.send(self.agent.send_message(controller_agent_name, f"bulb_brightness:{bulb_brightness}"))
                print(f"\n\nBulb agent ---> Control agent : bulb_brightness:{bulb_brightness}")
                messages.append(f"Bulb agent ---> Control agent : bulb_brightness:{bulb_brightness}")

                
                await asyncio.sleep(2)
                 
                # receiving the strategy from the controller agent   
                strategy_msg = await self.receive(timeout=10)
                while strategy_msg is None or not strategy_msg.body.startswith("strategy:"):
                    strategy_msg = await self.receive(timeout=10)
                    
                strategy =  strategy_msg.body.split(":")[1]
                print(f"\n[BulbAgent] Received strategy: {strategy}")
                
                if strategy == "BA" or strategy == "BF" :
                    bulb_active = True
                    print(f"\n[BulbAgent] The bulb will be turned on with {bulb_brightness} brightness ")
                    messages.append(f"[BulbAgent] The bulb will be turned on with {bulb_brightness} brightness ")
                elif strategy == "WB" or strategy == "WFB":
                    bulb_active = True
                    bulb_brightness = bulb_brightness*0.85
                    print(f"\n[BulbAgent] The bulb will be turned on with {bulb_brightness} brightness ")
                    messages.append(f"[BulbAgent] The bulb will be turned on with {bulb_brightness} brightness ")
                else:
                    bulb_active = False
                    print("\n[BulbAgent] The bulb will be turned off ")
                    messages.append("[BulbAgent] The bulb will be turned off ")
                    
                brightness = bulb_brightness
                
                finish_agents_count += 1
                
                bulb_agent_active = False
                while not bulb_agent_active:
                    await asyncio.sleep(1)
                    
                # self.agent.init()
                # await self.agent.stop()
                # await asyncio.sleep(main_agents_skip_time)
                
                
                
            

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=2)
        b = self.ManageBulb(period=2, start_at=start_at)
        self.add_behaviour(b)


class ControllerAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.win_decision = None
        self.fan_power = None
        self.ac_power = None
        self.bulb_brightness = None
        
    def init(self): 
        self.win_decision = None
        self.fan_power = None
        self.ac_power = None
        self.bulb_brightness = None
    
    def send_message(self, to, content):
        msg = Message(to=to)  # Receiver's JID
        msg.set_metadata("performative", "inform")  # Message type
        msg.body = content  # Message body
        return msg
        

    # Method to handle incoming messages
    def receive_message(self, msg): 
        if msg is not None:
            if msg.body.startswith("win_decision:"):
                self.win_decision = float(msg.body.split(":")[1])
            elif msg.body.startswith("fan_power:"):
                self.fan_power = float(msg.body.split(":")[1])
            elif msg.body.startswith("ac_power:"):
                self.ac_power = float(msg.body.split(":")[1])
            elif msg.body.startswith("bulb_brightness:"):
                self.bulb_brightness = float(msg.body.split(":")[1])
            #print(f"[WindowsAgent] Received - Brightness: {self.brightness}, Temperature: {self.temperature}, Humidity: {self.humidity}")
    
    # Cyclic behaviour to manage window decision based on the received values
    class ManageController(PeriodicBehaviour):
        async def run(self):
            
            global controller_agent_active, messages, finish_agents_count
            # Call receive_message to catch incoming sensor data
            self.agent.receive_message(await self.receive(timeout=10))
            
            current_time = datetime.datetime.now()
            
            # Ensure that all necessary values are received
            if self.agent.win_decision is not None and self.agent.fan_power is not None and self.agent.ac_power is not None and self.agent.bulb_brightness is not None:
                
                print(f"\n\n\n[ControllerAgent] Received :: win_decision: {self.agent.win_decision}, fan_power: {self.agent.fan_power}, ac_power: {self.agent.ac_power}, bulb_brightness: {self.agent.bulb_brightness}")

                # Calculate decision and importance
                if self.agent.win_decision > 0.5 and current_time.hour >= 7 and current_time.hour < 16:
                    if self.agent.fan_power >50 and self.agent.bulb_brightness<200:
                        strategy = "WF"
                    elif self.agent.fan_power >50 and self.agent.bulb_brightness>200:
                        strategy = "WFB"
                    elif self.agent.fan_power <50 and self.agent.bulb_brightness>200:
                        strategy = "WB"
                    else:
                        strategy = "W"
                else:
                    if self.agent.fan_power < self.agent.ac_power and self.agent.bulb_brightness > 0:
                        strategy = "BF"
                    elif self.agent.fan_power > self.agent.ac_power and self.agent.bulb_brightness > 0:
                        strategy = "BA"
                    elif self.agent.fan_power < self.agent.ac_power and self.agent.bulb_brightness <= 0:
                        strategy = "F"
                    elif self.agent.fan_power > self.agent.ac_power and self.agent.bulb_brightness <= 0:
                        strategy = "A"
                
                await self.send(self.agent.send_message(ac_agent_name, f"strategy:{strategy}"))
                print(f"\nControl agent ---> AC agent : strategy:{strategy}")
                messages.append(f"Control agent ---> AC agent : strategy:{strategy}")
                
                await self.send(self.agent.send_message(fan_agent_name, f"strategy:{strategy}"))
                print(f"\n Control agent ---> Windows agent : strategy:{strategy}")
                messages.append(f"Control agent ---> Windows agent : strategy:{strategy}")
                
                await self.send(self.agent.send_message(bulb_agent_name, f"strategy:{strategy}"))
                print(f"\n Control agent ---> Fan agent : strategy:{strategy}")
                messages.append(f"Control agent ---> Fan agent : strategy:{strategy}")
                
                await self.send(self.agent.send_message(win_agent_name, f"strategy:{strategy}"))
                print(f"\n Control agent ---> Bulb agent : strategy:{strategy}")
                messages.append(f"Control agent ---> Bulb agent : strategy:{strategy}")
                
                controller_agent_active = False
                while not controller_agent_active:
                    await asyncio.sleep(1)
                
                self.agent.init()
                # await self.agent.stop()
                # await asyncio.sleep(main_agents_skip_time)
                
                

    async def setup(self):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        b = self.ManageController(period=2, start_at=start_at)
        self.add_behaviour(b)
        
 

# Handle Slider Movement
# def handle_slider(slider_rect, value, min_val, max_val):
#     mouse_x, mouse_y = pygame.mouse.get_pos()
#     if pygame.mouse.get_pressed()[0] and slider_rect.collidepoint(mouse_x, slider_rect.y):
#         new_value = min_val + (max_val - min_val) * (mouse_x - slider_rect.x) / SLIDER_WIDTH
#         return int(new_value)
#     return value

def handle_slider(slider_rect, value, min_val, max_val):
    global current_slider

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Left mouse button pressed
        if current_slider is None and slider_rect.collidepoint(mouse_x, mouse_y):
            current_slider = slider_rect  # Set the active slider
        if current_slider == slider_rect:  # Update only the active slider
            new_value = min_val + (max_val - min_val) * (mouse_x - slider_rect.x) / SLIDER_WIDTH
            return max(min(int(new_value), max_val), min_val)  # Clamp the value within range
    else:
        if current_slider == slider_rect:  # Reset active slider when the mouse is released
            current_slider = None

    return value


# Draw Sliders
def draw_slider(slider_rect, value, min_val, max_val, label):
    pygame.draw.rect(screen, GRAY, slider_rect)  # Slider background
    handle_x = slider_rect.x + (value - min_val) / (max_val - min_val) * SLIDER_WIDTH
    pygame.draw.circle(screen, BLUE, (int(handle_x), slider_rect.y + SLIDER_HEIGHT // 2), 10)  # Slider handle
    text_surface = FONT.render(f"{label}: {value}", True, BLACK)
    screen.blit(text_surface, (slider_rect.x, slider_rect.y - 25))
    
    
# Pygame Loop Function
async def pygame_loop():
    global fan_active, ac_active, window_open, bulb_active, messages, temp, humidity, light, agents_started, outside_brightness, agents_task, finish_agents_count, ac_power, fan_power, brightness, ac_agent_active, fan_agent_active, win_agent_active, bulb_agent_active, controller_agent_active, light_agent_active, temp_agent_active, hum_agent_active, ac_agent_active, fan_agent_active, win_agent_active, bulb_agent_active, controller_agent_active

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not agents_started and button_rect.collidepoint(event.pos):
                    # Trigger agent startup when the button is clicked
                    if not agents_started:
                        messages.append("Agents starting...")
                        agents_started = True
                        
                if agents_started and finish_agents_count == 4 and button_rect.collidepoint(event.pos):
                    
                    messages = []
                    
                    finish_agents_count = 0
                    ac_active = False
                    fan_active = False
                    window_open = False
                    bulb_active = False
                    ac_power = None
                    fan_power = None
                    brightness = None
                    agents_started = True
                    
                    light_agent_active = True
                    temp_agent_active = True
                    hum_agent_active = True
                    ac_agent_active = True
                    fan_agent_active = True
                    win_agent_active = True
                    bulb_agent_active = True
                    controller_agent_active = True
                    
                    messages.append("Restart complete...")
                    
    
                    
                
                        
        # Update Slider Values
        temp = handle_slider(temp_slider_rect, temp, 15, 40)
        humidity = handle_slider(humidity_slider_rect, humidity, 20, 90)
        light = handle_slider(light_slider_rect, light, 100, 800)
        outside_brightness = handle_slider(outside_brightness_slider_rect, outside_brightness, 100, 800)
        

        # Display Components
        # Fan
        if fan_active:
            screen.blit(fan_active_img, fan_pos)
            fan_status = "Fan is active now with power " + str(fan_power)
        else:
            screen.blit(fan_img, fan_pos)
            fan_status = "Fan is inactive"
        fan_status_text = FONT.render(fan_status, True, BLACK)
        screen.blit(fan_status_text, (fan_pos[0] + 120, fan_pos[1] + 40))

        # A/C
        if ac_active:
            screen.blit(ac_active_img, ac_pos)
            ac_status = f"A/C is active now with {ac_power} power"
        else:
            screen.blit(ac_img, ac_pos)
            ac_status = "A/C is inactive"
        ac_status_text = FONT.render(ac_status, True, BLACK)
        screen.blit(ac_status_text, (ac_pos[0] + 120, ac_pos[1] + 40))

        # Window
        if window_open:
            screen.blit(window_active_img, window_pos)
            window_status = "Window is open"
        else:
            screen.blit(window_img, window_pos)
            window_status = "Window is closed"
        window_status_text = FONT.render(window_status, True, BLACK)
        screen.blit(window_status_text, (window_pos[0] + 120, window_pos[1] + 40))

        # Bulb
        if bulb_active:
            screen.blit(bulb_active_img, bulb_pos)
            bulb_status = f"Bulb is on with brightness {brightness} lux"
        else:
            screen.blit(bulb_img, bulb_pos)
            bulb_status = "Bulb is off"
        bulb_status_text = FONT.render(bulb_status, True, BLACK)
        screen.blit(bulb_status_text, (bulb_pos[0] + 120, bulb_pos[1] + 40))
        
        # Message Log
        pygame.draw.rect(screen, GRAY, (453, 10, 580, 700))
        y = 30
        if len(messages) > 20:
            for msg in messages[-20:]:  # Show last 20 messages
                msg_surface = FONT.render(msg, True, BLACK)
                screen.blit(msg_surface, (455, y))
                y += 30
        else:
            for msg in messages:
                msg_surface = FONT.render(msg, True, BLACK)
                screen.blit(msg_surface, (455, y))
                y += 30
                
        # Draw Start Button (Enabled or Disabled)
        if agents_started and finish_agents_count < 4:
            # Render a disabled button (gray color)
            pygame.draw.rect(screen, GRAY, button_rect)
            button_text_surface = FONT.render("Agents Started", True, BLACK)
            
        elif agents_started and finish_agents_count == 4:
            # Render a disabled button (gray color)
            pygame.draw.rect(screen, RED, button_rect)
            button_text_surface = FONT.render("Restart Agents", True, WHITE)
        else:
            # Render an active button (blue color)
            pygame.draw.rect(screen, BLUE, button_rect)
            button_text_surface = FONT.render("Start Agents", True, WHITE)
        screen.blit(button_text_surface, (button_rect.x + 20, button_rect.y + 15))

        # Draw Sliders
        draw_slider(temp_slider_rect, temp, 15, 40, "Temperature")
        draw_slider(humidity_slider_rect, humidity, 20, 90, "Humidity")
        draw_slider(light_slider_rect, light, 100, 800, "Room Brightness")
        draw_slider(outside_brightness_slider_rect, outside_brightness, 100, 800, "Outside Brightness")
      
        # Update Display
        pygame.display.flip()
        clock.tick(10)  # 30 FPS
        
        # Yield control to the event loop
        await asyncio.sleep(0.01) 



async def start_agents():
    # Create agents
    temperature_agent = TemperatureSensorAgent(temp_agent_name, temp_agent_password)
    humidity_agent = HumiditySensorAgent(hum_agent_name, hum_agent_password)
    light_sensor_agent = LightSensorAgent(light_agent_name, light_agent_password)
    ac_agent = ACAgent(ac_agent_name, ac_agent_password, FuzzyLogic())
    fan_agent = FanAgent(fan_agent_name, fan_agent_password, FuzzyLogic())
    windows_agent = WindowsAgent(win_agent_name, win_agent_password, FuzzyLogic())
    bulb_agent = BulbAgent(bulb_agent_name, bulb_agent_password, FuzzyLogic())
    controller_agent = ControllerAgent(controller_agent_name, controller_agent_password)

    agents = [temperature_agent, humidity_agent, light_sensor_agent, ac_agent, fan_agent, windows_agent, bulb_agent, controller_agent]

    # Start all agents
    await asyncio.gather(*(agent.start() for agent in agents))



    # Keep agents running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Stop agents gracefully
        for agent in agents:
            await agent.stop()

async def main():
    global agents_started, agents_task, messages

    try:
        # Run the Pygame loop as a task
        pygame_task = asyncio.create_task(pygame_loop())  # Run Pygame loop

        # Wait for agents to be started (i.e., wait for button click)
        while not agents_started:
            await asyncio.sleep(0.1)  # Non-blocking wait for the button press

        # Start the agents once the button is pressed
        agents_task = asyncio.create_task(start_agents())

        # Wait for all tasks to complete (Pygame loop and agents)
        await asyncio.gather(pygame_task, agents_task)

    except asyncio.CancelledError:
        print("[main] Agents task was canceled.")
        # Ensure all cleanup happens if needed, this might include clearing any flags for button state
        agents_started = False  # Reset the state of agents_started to allow starting again

    finally:
        print("[main] Exiting main function.")
        # Reset button state to blue after restart
        messages.append("Restart complete, click 'Start Agents' to start again.")

if __name__ == "__main__":
    #main()
    asyncio.run(main())
