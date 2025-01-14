import pygame as pg

class Button:
    def __init__(self, rect, screen_size, background=(255, 0, 0), command=lambda: print("clicked"), border_radius=0, transparent=False, image_scale=1, image_rotation=0, bump_on_click=False, ):
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
        self.original_image = pg.Surface(self.rect.size, pg.SRCALPHA)  # Support alpha channel

        # Handle background as color or image
        if isinstance(background, tuple):  # RGB tuple
            if transparent:
                self.original_image.fill((0, 0, 0, 0))  # Fully transparent
            else:
                self.original_image.fill((0, 0, 0))  # Opaque background for masking
                self.original_image.set_colorkey((0, 0, 0))  # Make the black background invisible
                pg.draw.rect(self.original_image, background, (0, 0, self.rect.width, self.rect.height), border_radius=border_radius)
        elif isinstance(background, str):  # Image path
            bg_image = pg.image.load(background).convert_alpha()

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
            raise ValueError("The background must be an RGB tuple or a path to an image.")

        self.image = self.original_image.copy()

        # Create the mask for click detection
        mask_surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(mask_surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height), border_radius=border_radius)
        self.mask = pg.mask.from_surface(mask_surface)

    def render(self, screen):
        """Render the button onto the screen."""
        screen.blit(self.image, self.rect)

    def get_event(self, event):
        """Handle events for the button."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            rel_x, rel_y = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:  # Bounds check
                if self.mask.get_at((rel_x, rel_y)):
                    if self.bump_on_click:
                        self._bump_effect()
                    self.command()

    def _bump_effect(self):
        """Create a bump effect by temporarily scaling the button."""
        enlarged_width = int(self.rect.width * 1.1)  # 10% larger
        enlarged_height = int(self.rect.height * 1.1)
        bumped_image = pg.transform.scale(self.original_image, (enlarged_width, enlarged_height))

        # Center the bumped image on the original rect
        offset_x = (enlarged_width - self.rect.width) // 2
        offset_y = (enlarged_height - self.rect.height) // 2
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
        self.image.blit(bumped_image, (-offset_x, -offset_y))

        # Restore the original image after a short delay
        pg.time.set_timer(pg.USEREVENT + 1, 100)  # 100ms delay

    def reset_bump(self):
        """Reset the bump effect back to the original image."""
        self.image = self.original_image.copy()
