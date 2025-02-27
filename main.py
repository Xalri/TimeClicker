from engine import Engine
from paintStrategy import PaintStrategy


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
    main()
