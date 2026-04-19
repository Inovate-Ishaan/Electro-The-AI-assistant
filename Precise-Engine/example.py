#!/usr/bin/env python3
# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from argparse import ArgumentParser
#from precise.util import activate_notify
from precise_runner import PreciseRunner, PreciseEngine
from threading import Event


def main():
    # parser = ArgumentParser('Implementation demo of precise-engine he he he he he')
    # parser.add_argument('engine', help='Location of binary engine file')
    # parser.add_argument('model')
    # args = parser.parse_args()

    def on_prediction(prob):
        pass
    def on_activation():
        #activate_notify()
        print("Active")

    model_path_hey_comp = "model_files/hey_computer_model/heycomputer-es.pb"
    model_path_hey_mycroft = "model_files/hey-mycroft-2/hey-mycroft-2.pb"
    engine_path = "precise-engine_0.3/precise-engine/precise-engine"
    engine = PreciseEngine(engine_path, model_path_hey_mycroft)
    PreciseRunner(engine, on_prediction=on_prediction, on_activation=on_activation,
                  trigger_level=0).start()
    Event().wait()  # Wait forever


if __name__ == '__main__':
    main()
