import wx
import random
import os
from ebird_api import get_recent_observations

class MainMenu(wx.Frame):
    def __init__(self, parent, title):
        super(MainMenu, self).__init__(parent, title=title, size=(400, 600))
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint_background)
        
        start_btn = wx.Button(self.panel, label="Start", pos=(150, 280))
        start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        
        self.switch_bg_btn = wx.Button(self.panel, label="Switch BG", pos=(10, 550))
        self.switch_bg_btn.Bind(wx.EVT_BUTTON, self.switch_background)
        
        self.backgrounds = [
            wx.Image("graphics/backgrounds/sky.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
            wx.Image("graphics/backgrounds/woods.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        ]
        self.current_bg_index = 0

        self.location_code_text = wx.TextCtrl(self.panel, value="US-IL-031", pos=(50, 50), size=(300, 20))

        self.fetch_birds_btn = wx.Button(self.panel, label="Fetch Recent Birds", pos=(150, 80))
        self.fetch_birds_btn.Bind(wx.EVT_BUTTON, self.fetch_recent_birds)   
        
        self.recent_birds_display = wx.StaticText(self.panel, label="", pos=(50, 390))

        bird_sprite_files = os.listdir("graphics/bird sprites")

        self.bird_images_dict = {
            os.path.splitext(filename)[0]: wx.Image(f"graphics/bird sprites/{filename}", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            for filename in bird_sprite_files
            if not filename.startswith('.')
        }

        self.placeholder_image = wx.Image("graphics/bird sprites/___.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        bird_sprite_files = [f for f in os.listdir("graphics/bird sprites/") if f.endswith(".png")]
        self.bird_images = [wx.Image(f"graphics/bird sprites/{filename}", wx.BITMAP_TYPE_ANY).ConvertToBitmap() for filename in bird_sprite_files]
        bird_names = [os.path.splitext(filename)[0] for filename in bird_sprite_files]
        self.bird_choice = wx.Choice(self.panel, choices=bird_names, pos=(150, 250))
        self.bird_choice.SetSelection(0)

    def fetch_recent_birds(self, event):
        region_code = self.location_code_text.GetValue()
        recent_birds = get_recent_observations(region_code)

        if recent_birds:
            playable_birds = []
            for bird in recent_birds:
                if bird in self.bird_images_dict:
                    playable_birds.append(bird)
                else:
                    playable_birds.append(f"{bird} (placeholder)")

            self.bird_choice.SetItems(playable_birds)
            self.bird_choice.SetSelection(0)

            self.recent_birds_display.SetLabel("\n".join(recent_birds))
        else:
            wx.MessageBox('Failed to fetch recent birds or no recent observations found.', 'Error', wx.OK | wx.ICON_ERROR)
    
    def on_start(self, event):
        selected_bird_name = self.bird_choice.GetStringSelection()
        
        if "(placeholder)" in selected_bird_name:
            chosen_bird_image = self.placeholder_image
        else:
            selected_bird_name = selected_bird_name.replace(" (placeholder)", "")
            chosen_bird_image = self.bird_images_dict.get(selected_bird_name, self.placeholder_image)

        self.game_window = GameWindow(None, "Angr eBirds", self.current_bg_index, chosen_bird_image)
        self.game_window.Show()
        self.Close()

    def on_paint_background(self, event):
        dc = wx.PaintDC(self.panel)
        dc.Clear()
        dc.DrawBitmap(self.backgrounds[self.current_bg_index], 0, 0)

    def switch_background(self, event):
        self.current_bg_index += 1
        if self.current_bg_index >= len(self.backgrounds):
            self.current_bg_index = 0
        self.Refresh()


class GameWindow(wx.Frame):
    def __init__(self, parent, title, current_bg_index=0, chosen_bird_image=None):
        super(GameWindow, self).__init__(parent, title=title, size=(400, 600))

        self.score = 0
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.panel.SetFocus()
        self.chosen_bird_image = chosen_bird_image

        # Bird properties
        self.bird_position = 300
        self.bird_velocity = 0
        self.gravity = 0.5

     # Background properties
        self.backgrounds = [wx.Image("graphics/backgrounds/sky.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
                            wx.Image("graphics/backgrounds/woods.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()]
        self.current_bg_index = current_bg_index
        self.background_image = self.backgrounds[self.current_bg_index]
        self.background_x = 0  # starting position
        self.background_scroll_speed = 1  # adjust this for desired scroll speed

        # Obstacle properties
        self.obstacle_width = 75
        self.obstacle_gap = 200
        self.obstacle_x = 400
        self.obstacle_height = random.randint(100, 400)
        self.building_image = wx.Image("graphics/obstacles/building.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.log_image = wx.Image("graphics/obstacles/log.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.current_obstacle_image = self.building_image  # default

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(16)

    def on_key_down(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            self.jump()
        event.Skip()

    def jump(self):
        self.bird_velocity = -8

    def update(self, event):
        self.bird_position += self.bird_velocity
        self.bird_velocity += self.gravity

        self.obstacle_x -= 5
        if self.obstacle_x + self.obstacle_width < 0:
            self.obstacle_x = 400
            
            max_obstacle_height = self.panel.GetSize()[1] - self.obstacle_gap  # To make sure gap is not out of screen
            self.obstacle_height = random.randint(100, max_obstacle_height)  # min of 100 for aesthetics
            
            self.score += 1

        # Update the x-coordinate of the background
        self.background_x -= self.background_scroll_speed
        if self.background_x <= -self.background_image.GetWidth():
            self.background_x = 0

        # Collision detection
        bird_radius = 0
        bird_x = 200

        if (bird_x + bird_radius > self.obstacle_x and bird_x - bird_radius < self.obstacle_x + self.obstacle_width):
            if self.bird_position - bird_radius < self.obstacle_height or self.bird_position + bird_radius > self.obstacle_height + self.obstacle_gap:
                self.timer.Stop()
                self.go_to_main_menu()

        self.Refresh()

    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        dc.Clear()

        # Draw the scrolling background
        dc.DrawBitmap(self.background_image, self.background_x, 0)
        # Draw the repeating section of the background to fill any gaps
        if self.background_x + self.background_image.GetWidth() < 400:  # assuming the game width is 400
            dc.DrawBitmap(self.background_image, self.background_x + self.background_image.GetWidth(), 0)

        # Draw the bird
        if self.chosen_bird_image:
            bird_width = self.chosen_bird_image.GetWidth()
            bird_height = self.chosen_bird_image.GetHeight()
            dc.DrawBitmap(self.chosen_bird_image, 200 - bird_width/2, self.bird_position - bird_height/2)
        # dc.DrawCircle(200, self.bird_position, 20)

        if self.current_bg_index == 0:  # Let's say the building is for the sky background
            # Top obstacle
            top_obstacle_y = self.obstacle_height - self.building_image.GetHeight()
            dc.DrawBitmap(self.building_image, self.obstacle_x, top_obstacle_y)
            
            # Bottom obstacle
            bottom_obstacle_y = self.obstacle_height + self.obstacle_gap
            dc.DrawBitmap(self.building_image, self.obstacle_x, bottom_obstacle_y)

        else:  # The log is for the woods background
            # Top obstacle
            top_obstacle_y = self.obstacle_height - self.log_image.GetHeight()
            dc.DrawBitmap(self.log_image, self.obstacle_x, top_obstacle_y)
            
            # Bottom obstacle
            bottom_obstacle_y = self.obstacle_height + self.obstacle_gap
            dc.DrawBitmap(self.log_image, self.obstacle_x, bottom_obstacle_y)

        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(wx.Colour(255, 255, 255))  # White color
        score_text = f"Score: {self.score}"
        text_width, text_height = dc.GetTextExtent(score_text)
        dc.DrawText(score_text, 400 - text_width - 10, 10)

    def go_to_main_menu(self):
        main_menu = MainMenu(None, "Main Menu")
        main_menu.Show()
        self.Close()

if __name__ == "__main__":
    app = wx.App(False)
    main_frame = MainMenu(None, title='Angr eBirds - Main Menu')
    main_frame.Show()
    app.MainLoop()