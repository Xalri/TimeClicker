from engine.engine import Engine
from ihm.paintStrategy import PaintStrategy
import os
import sys
import ctypes



def get_dependencies_folder():
    if getattr(sys, 'frozen', False):
        exe_folder = os.path.dirname(sys.executable)
    else:
        exe_folder = os.path.dirname(os.path.realpath(__file__))

    appdata_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'MyApp', 'dependencies')
    
    if os.path.exists(appdata_folder):
        print(f"Found dependencies in AppData at: {appdata_folder}")
        return appdata_folder
    else:
        print("Dependencies not found in AppData.")
        return None

def load_dependency(dependency_folder):
    dependency_file = os.path.join(dependency_folder, 'your_dependency.dll')
    
    if os.path.exists(dependency_file):
        print(f"Found dependency: {dependency_file}")
        ctypes.CDLL(dependency_file)
    else:
        print(f"Dependency not found: {dependency_file}")



def main():
    engine = Engine()
    paintstrategy = PaintStrategy(engine, engine.screen, engine.src_dir)

    engine.load_data()
    engine.give_timeUnits_from_afk()

    while engine.running:
        engine.clock.tick_busy_loop(engine.framerate)
        
        engine.update()
        
        engine.check_era()
        
        engine.check_cables()
        
        engine.check_era()
        
        
        paintstrategy.init_screen()

        engine.check_available_buildings()
        engine.check_available_upgrades()

        paintstrategy.create_buildings_buttons()
        paintstrategy.create_upgrades_buttons()
        paintstrategy.create_human_skills_buttons()
        
        engine.add_cable_boost()

        engine.handle_human_skills()

        paintstrategy.update_elements()


        paintstrategy.handle_event()

        paintstrategy.check_mouse_hover()

        paintstrategy.display_back_images()

        paintstrategy.display_buildings()
        paintstrategy.display_upgrades()

        paintstrategy.display_front_elements()
        
        paintstrategy.display_human_skills()

        paintstrategy.display_info_box()
        
        paintstrategy.display_cables()

        paintstrategy.update_screen()
    
        engine.check_autosave()


if __name__ == "__main__":
    
    dependencies_folder = get_dependencies_folder()

    if dependencies_folder:
        print("Loading dependencies...")
        load_dependency(dependencies_folder)

    
    main()
