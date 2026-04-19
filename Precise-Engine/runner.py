from precise_runner import PreciseEngine, PreciseRunner
from main_scripts import main

engine = PreciseEngine('/project_electro/Electro---The-AI-assistant/Precise-Engine/precise-engine_0.3/precise-engine/precise-engine', '/project_electro/Electro---The-AI-assistant/Precise-Engine/model_files/hey-mycroft-2/hey-mycroft-2.pb')
runner = PreciseRunner(engine, on_activation=main.main)
runner.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)