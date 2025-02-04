import pygame as pg
from utils import load_image


class Button:
    def __init__(self, rect, screen_size: tuple[int, int], background=(255, 0, 0), command=lambda: print("clicked"), border_radius=0, transparent=False, image_scale=1, image_rotation=0, bump_on_click=False, identifier=None):
        """
        Initialize the button.

        :param rect: The rectangle specifying the button's position and size.
        :param background: The button background, either an RGB tuple or a path to an image.
        :param command: The function to execute when the button is clicked.
        :param border_radius: The border radius for rounded corners (only used for color backgrounds).
        :param transparent: Whether the button should be transparent.
        :param image_scale: A scaling factor to resize the background image (default is 1, meaning no scaling).
        :param image_rotation: The angle in degrees to rotate the image (default is 0, meaning no rotation).
        :param bump_on_click: Whether the button should visually "bump" when clicked (default is False).
        """
        self.rect = pg.Rect(rect)
        self.command = command
        self.bump_on_click = bump_on_click
        self.is_bumping = False
        self.original_image = pg.Surface(self.rect.size, pg.SRCALPHA)  # Support alpha channel
        self.bump_event = pg.USEREVENT + 1  # Timer event for bump reset
        self.identifier = identifier
        self.hovering = False


        # Handle background as color or image
        if isinstance(background, tuple):  # RGB tuple
            if transparent:
                self.original_image.fill((0, 0, 0, 0))  # Fully transparent
            else:
                self.original_image.fill((0, 0, 0))  # Opaque background for masking
                self.original_image.set_colorkey(
                    (0, 0, 0)
                )  # Make the black background invisible
                pg.draw.rect(
                    self.original_image,
                    background,
                    (0, 0, self.rect.width, self.rect.height),
                    border_radius=border_radius,
                )
        elif isinstance(background, str):  # Image path
            bg_image = load_image(background, screen_size[0], screen_size[1])

            # Scale the image while preserving aspect ratio
            if isinstance(image_scale, (int, float)) and image_scale > 0:
                new_width = int(bg_image.get_width() * image_scale)
                new_height = int(bg_image.get_height() * image_scale)
                scaled_image = pg.transform.scale(bg_image, (new_width, new_height))
            else:
                raise ValueError("image_scale must be a positive number.")

            # Rotate the image
            if isinstance(image_rotation, (int, float)):
                rotated_image = pg.transform.rotate(scaled_image, image_rotation)
            else:
                raise ValueError("image_rotation must be a number.")

            # Center the transformed image on the button
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

    def render(self, screen, darker=False):
        """Render the button onto the screen."""
        if darker:
            image = self.image
            image.fill((100,100,100), special_flags=pg.BLEND_MULT)
        else:
            image = self.image
        screen.blit(image, self.rect)

    def get_event(self, event):
        """Handle events for the button."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            rel_x, rel_y = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:
                if self.mask.get_at((rel_x, rel_y)):
                    if self.bump_on_click and not self.is_bumping:
                        self._bump_effect()
                    self.command()

        if event.type == pg.USEREVENT + 1:
            self.reset_bump()

        if event.type == pg.MOUSEMOTION:
            self.update_hover_state(event.pos)

    def update_hover_state(self, mouse_pos):
        """Update hover state and set the cursor accordingly."""
        rel_x, rel_y = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        hovering = 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height and self.mask.get_at((rel_x, rel_y))

        if hovering:
            if not self.hovering:  # Prevent redundant calls
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.hovering = True
        else:
            if self.hovering:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.hovering = False



    def _bump_effect(self):
        """Create a bump effect by temporarily scaling the button."""
        self.is_bumping = True
        enlarged_width = int(self.rect.width * 1.1)  # 10% larger
        enlarged_height = int(self.rect.height * 1.1)
        bumped_image = pg.transform.scale(
            self.original_image, (enlarged_width, enlarged_height)
        )

        # Center the bumped image on the original rect
        offset_x = (enlarged_width - self.rect.width) // 2
        offset_y = (enlarged_height - self.rect.height) // 2
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
        self.image.blit(bumped_image, (-offset_x, -offset_y))

        # Restore the original image after a short delay
        pg.time.set_timer(self.bump_event, 0)

        # Restore the original image after a short delay
        pg.time.set_timer(self.bump_event, 100)

    def reset_bump(self):
        """Reset the bump effect back to the original image."""
        self.image = self.original_image.copy()
        self.is_bumping = False
        pg.time.set_timer(self.bump_event, 0)  # Stop the timer

