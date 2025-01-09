import pygame as pg

class Button:
    def __init__(self, rect, color=(255, 0, 0), command=lambda: print("clicked"), border_radius=0, transparent=False):
        """
        Initialize the button.
        
        :param rect: The rectangle specifying the button's position and size.
        :param color: The button color as an RGB tuple.
        :param command: The function to execute when the button is clicked.
        :param border_radius: The border radius for rounded corners.
        :param transparent: Whether the button should be transparent.
        """
        self.color = color
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)  # Support alpha channel
        
        # Create the visible surface
        if transparent:
            self.image.fill((0, 0, 0, 0))  # Fully transparent
        else:
            self.image.fill((0, 0, 0))  # Opaque background for masking
            self.image.set_colorkey((0, 0, 0))  # Make the black background invisible
            pg.draw.rect(self.image, color, (0, 0, self.rect.width, self.rect.height), border_radius=border_radius)

        # Create the mask for click detection
        mask_surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(mask_surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height), border_radius=border_radius)
        self.mask = pg.mask.from_surface(mask_surface)

        self.command = command

    def render(self, screen):
        """Render the button onto the screen."""
        screen.blit(self.image, self.rect)

    def get_event(self, event):
        """Handle events for the button."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            rel_x, rel_y = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if 0 <= rel_x < self.rect.width and 0 <= rel_y < self.rect.height:  # Bounds check
                if self.mask.get_at((rel_x, rel_y)):
                    self.command()


# Example
# button = Button((100, 100, 200, 50), border_radius=10, transparent=True)
