import pygame as pg
from engine.utils import load_image, get_text_font, adapt_size_height, adapt_size_width


class Button:
    def __init__(self, rect, screen_size: tuple[int, int], background=(255, 0, 0), command=lambda: print("clicked"), border_radius=0, transparent=False, image_scale=1, image_rotation=0, bump_on_click=False, circle_on_click=False, identifier=None, infos=""):
        """
        Initialize the button.

        :param rect: The rectangle specifying the button's position and size.
        :param tuple[int, int] screen_size: The size of the screen.
        :param background: The button background, either an RGB tuple or a path to an image.
        :param command: The function to execute when the button is clicked.
        :param int border_radius: The border radius for rounded corners (only used for color backgrounds).
        :param bool transparent: Whether the button should be transparent.
        :param float image_scale: A scaling factor to resize the background image (default is 1, meaning no scaling).
        :param float image_rotation: The angle in degrees to rotate the image (default is 0, meaning no rotation).
        :param bool bump_on_click: Whether the button should visually "bump" when clicked (default is False).
        :param bool circle_on_click: Whether a circle should appear at the click position and fade out (default is False).
        :param identifier: An optional identifier for the button.
        :param str infos: Additional information to display when hovering over the button.
        """
        self.rect = pg.Rect(rect)
        self.command = command
        self.bump_on_click = bump_on_click
        self.circle_on_click = circle_on_click
        self.is_bumping = False
        self.original_image = pg.Surface(self.rect.size, pg.SRCALPHA)  # Support alpha channel
        self.bump_event = pg.USEREVENT + 1  # Timer event for bump reset
        self.circle_event = pg.USEREVENT + 2  # Timer event for circle fade out
        self.identifier = identifier
        self.hovering = False
        self.display_info = False
        self.infos = infos
        self.mouse_pos = (0, 0)
        self.circle_alpha = 255
        self.circle_pos = (0, 0)
        self.circles = []

        if isinstance(background, tuple):
            if transparent:
                self.original_image.fill((0, 0, 0, 0))
            else:
                self.original_image.fill((0, 0, 0))
                self.original_image.set_colorkey(
                    (0, 0, 0)
                )
                pg.draw.rect(
                    self.original_image,
                    background,
                    (0, 0, self.rect.width, self.rect.height),
                    border_radius=border_radius,
                )
        elif isinstance(background, str):
            bg_image = load_image(background, screen_size[0], screen_size[1])

            if isinstance(image_scale, (int, float)) and image_scale > 0:
                new_width = int(bg_image.get_width() * image_scale)
                new_height = int(bg_image.get_height() * image_scale)
                scaled_image = pg.transform.scale(bg_image, (new_width, new_height))
            else:
                raise ValueError("image_scale must be a positive number.")

            if isinstance(image_rotation, (int, float)):
                rotated_image = pg.transform.rotate(scaled_image, image_rotation)
            else:
                raise ValueError("image_rotation must be a number.")

            image_x = (self.rect.width - rotated_image.get_width()) // 2
            image_y = (self.rect.height - rotated_image.get_height()) // 2
            self.original_image.blit(rotated_image, (image_x, image_y))
        else:
            raise ValueError(
                "The background must be an RGB tuple or a path to an image."
            )

        self.image = self.original_image.copy()

        # Create the mask for click detection
        mask_surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(
            mask_surface,
            (255, 255, 255),
            (0, 0, self.rect.width, self.rect.height),
            border_radius=border_radius,
        )
        self.mask = pg.mask.from_surface(mask_surface)

    def render(self, screen, darker=False, w=1, h=1):
        """
        Render the button onto the screen.

        :param screen: The screen to render the button on.
        :param bool darker: Whether to render the button in a darker shade.
        :param float w: Width scaling factor.
        :param float h: Height scaling factor.
        """
        image = self.image
        if darker:
            image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
        screen.blit(image, self.rect)
        for circle in self.circles:
            circle_surface = pg.Surface((circle['radius'] * 2, circle['radius'] * 2), pg.SRCALPHA)
            pg.draw.circle(circle_surface, (255, 0, 0, circle['alpha']), (circle['radius'], circle['radius']), circle['radius'])
            screen.blit(circle_surface, (circle['pos'][0] - circle['radius'], circle['pos'][1] - circle['radius']))


    def render_infos(self, screen, darker=False, w=1, h=1):
        """
        Render additional information when hovering over the button.

        :param screen: The screen to render the information on.
        :param bool darker: Whether to render the information in a darker shade.
        :param float w: Width scaling factor.
        :param float h: Height scaling factor.
        """
        rel_x, rel_y = self.mouse_pos[0] - self.rect.x, self.mouse_pos[1] - self.rect.y
        hovering = 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height and self.mask.get_at((rel_x, rel_y))
        if hovering:
            texts = [get_text_font(15, h).render(text, True, (255, 255, 255)) for text in self.infos.split("\n")]
            max_width = max(text.get_width() for text in texts)
            total_height = sum(text.get_height() for text in texts) + (len(texts) - 1) * adapt_size_height(5, h)
            
            info_box = pg.Surface((max_width + 10, total_height + 10))
            info_box.fill((0, 0, 0))
            info_box.set_alpha(200)
            info_box_rect = info_box.get_rect(topleft=(self.mouse_pos[0] + adapt_size_width(10, w), self.mouse_pos[1]+adapt_size_height(10, h)))
            
            screen.blit(info_box, info_box_rect)
            
            y_offset = 5
            for text in texts:
                screen.blit(text, (info_box_rect.x + 5, info_box_rect.y + y_offset))
                y_offset += text.get_height() + adapt_size_height(5, h)

    def get_event(self, event):
        """
        Handle events for the button.

        :param event: The event to handle.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            rel_x, rel_y = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:
                if self.mask.get_at((rel_x, rel_y)):
                    if self.bump_on_click and not self.is_bumping:
                        self._bump_effect()
                    if self.circle_on_click:
                        self._circle_effect(event.pos)
                    self.command()

        elif event.type == pg.USEREVENT + 1:
            self._update_bump()
        
        elif event.type == pg.USEREVENT + 2:
            self._fade_circle()
            
        elif self.identifier == "clicker" and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if self.bump_on_click and not self.is_bumping:
                self._bump_effect()
            self.command()

    def update_hover_state(self, mouse_pos):
        """
        Update hover state and set the cursor accordingly.

        :param tuple[int, int] mouse_pos: The current mouse position.
        """
        rel_x, rel_y = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        hovering = 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height and self.mask.get_at((rel_x, rel_y))

        if hovering:
            if self.infos != "":
                self.display_info = True
                self.mouse_pos = mouse_pos
            if not self.hovering: 
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.hovering = True
            
            
        else:
            self.display_info = False
            if self.hovering:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.hovering = False

    def _bump_effect(self):
        """
        Create a smooth bump effect by gradually scaling the button.
        """
        self.is_bumping = True
        self.bump_scale = 1.0
        self.bump_direction = 1
        pg.time.set_timer(self.bump_event, 10)

    def _update_bump(self):
        """
        Update the bump effect by scaling the button.
        """
        if self.is_bumping:
            self.bump_scale += 0.02 * self.bump_direction
            if self.bump_scale >= 1.1:
                self.bump_direction = -1
            elif self.bump_scale <= 1.0:
                self.bump_direction = 0
                self.is_bumping = False
                pg.time.set_timer(self.bump_event, 0)
            
            enlarged_width = int(self.rect.width * self.bump_scale)
            enlarged_height = int(self.rect.height * self.bump_scale)
            bumped_image = pg.transform.scale(self.original_image, (enlarged_width, enlarged_height))

            offset_x = (enlarged_width - self.rect.width) // 2
            offset_y = (enlarged_height - self.rect.height) // 2
            self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
            self.image.blit(bumped_image, (-offset_x, -offset_y))

    def _circle_effect(self, pos):
        """
        Create a circle effect at the click position.

        :param tuple[int, int] pos: The position of the click.
        """
        self.circles.append({'pos': pos, 'alpha': 255, 'radius': 5})
        pg.time.set_timer(self.circle_event, 50)

    def _fade_circle(self):
        """
        Grow and fade out the circle effect.
        """
        for circle in self.circles:
            circle['alpha'] -= 25
            circle['radius'] += 5
        self.circles = [circle for circle in self.circles if circle['alpha'] > 0]
        if not self.circles:
            pg.time.set_timer(self.circle_event, 0)
        else:
            pg.time.set_timer(self.circle_event, 50)

    def reset_bump(self):
        """
        Reset the bump effect back to the original image.
        """
        self.image = self.original_image.copy()
        self.is_bumping = False
        pg.time.set_timer(self.bump_event, 0)