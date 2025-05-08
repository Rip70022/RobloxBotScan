# Roblox Server Bot Scanner | by x4x0 => Discord
from roblox import players, gui, analytics, game_service
import numpy as np
import time
from datetime import datetime

class BotDetectionSystem:
    def __init__(self):
        self.threshold_join_time = 5
        self.threshold_movement_pattern = 0.75
        self.threshold_chat_pattern = 0.8
        self.threshold_name_pattern = 0.7
        self.detection_interval = 30
        self.current_game_id = None
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = gui.create_frame("Bot Detection System", (800, 650))
        self.main_frame.set_background_color((40, 44, 52))
        
        self.title_label = gui.create_label(self.main_frame, "Advanced Bot Detection System", (20, 20), font_size=24, color=(220, 220, 220))
        
        # Game ID Input section
        self.input_frame = gui.create_frame_within(self.main_frame, (20, 70), (760, 60))
        self.input_frame.set_background_color((50, 54, 62))
        self.input_frame.set_border((60, 64, 72), 2)
        
        self.game_id_label = gui.create_label(self.input_frame, "Game ID:", (20, 20), font_size=16, color=(220, 220, 220))
        self.game_id_input = gui.create_text_input(self.input_frame, (120, 15), (400, 30))
        self.game_id_input.set_placeholder("Enter Roblox Game ID...")
        self.game_id_button = gui.create_button(self.input_frame, "Connect", (540, 15), action=self.connect_to_game)
        self.game_id_button.set_colors((65, 176, 230), (45, 50, 60))
        
        self.server_info_frame = gui.create_frame_within(self.main_frame, (20, 150), (760, 100))
        self.server_info_frame.set_background_color((50, 54, 62))
        self.server_info_frame.set_border((60, 64, 72), 2)
        
        self.server_name_label = gui.create_label(self.server_info_frame, "Server: Analyzing...", (20, 15), font_size=16, color=(220, 220, 220))
        self.player_count_label = gui.create_label(self.server_info_frame, "Players: 0/0", (20, 45), font_size=16, color=(220, 220, 220))
        self.last_scan_label = gui.create_label(self.server_info_frame, "Last scan: Never", (20, 75), font_size=12, color=(180, 180, 180))
        
        self.bot_percentage_frame = gui.create_frame_within(self.main_frame, (20, 270), (760, 100))
        self.bot_percentage_frame.set_background_color((50, 54, 62))
        self.bot_percentage_frame.set_border((60, 64, 72), 2)
        
        self.bot_percentage_label = gui.create_label(self.bot_percentage_frame, "Bot Percentage:", (20, 15), font_size=16, color=(220, 220, 220))
        self.bot_percentage_value = gui.create_label(self.bot_percentage_frame, "0%", (350, 15), font_size=36, color=(65, 176, 230))
        self.confidence_label = gui.create_label(self.bot_percentage_frame, "Detection confidence: Low", (20, 65), font_size=14, color=(180, 180, 180))
        
        self.progress_bar = gui.create_progress_bar(self.main_frame, (20, 390), (760, 30))
        self.progress_bar.set_colors((65, 176, 230), (50, 54, 62))
        self.progress_bar.set_value(0)
        
        self.details_frame = gui.create_frame_within(self.main_frame, (20, 440), (760, 170))
        self.details_frame.set_background_color((50, 54, 62))
        self.details_frame.set_border((60, 64, 72), 2)
        
        self.details_title = gui.create_label(self.details_frame, "Detection Details:", (20, 15), font_size=16, color=(220, 220, 220))
        self.join_time_detail = gui.create_label(self.details_frame, "Join Time Pattern: N/A", (30, 50), font_size=14, color=(180, 180, 180))
        self.movement_detail = gui.create_label(self.details_frame, "Movement Pattern: N/A", (30, 80), font_size=14, color=(180, 180, 180))
        self.chat_detail = gui.create_label(self.details_frame, "Chat Pattern: N/A", (30, 110), font_size=14, color=(180, 180, 180))
        self.name_detail = gui.create_label(self.details_frame, "Username Pattern: N/A", (30, 140), font_size=14, color=(180, 180, 180))
        
        self.button_frame = gui.create_frame_within(self.main_frame, (20, 630), (760, 50))
        self.button_frame.set_background_color((40, 44, 52))
        
        self.scan_button = gui.create_button(self.button_frame, "Start Continuous Scanning", (250, 10), action=self.toggle_continuous_scan)
        self.scan_button.set_colors((65, 176, 230), (45, 50, 60))
        self.scan_button.disable()  # Disabled until a game is connected
        
        self.status_label = gui.create_label(self.main_frame, "Status: Please enter a Game ID to begin", (20, 610), font_size=14, color=(180, 180, 180))
        
        self.is_scanning = False
        self.is_connected = False
        
    def analyze_join_times(self, players_list):
        join_times = [player.join_timestamp for player in players_list]
        join_times.sort()
        
        if len(join_times) <= 1:
            return 0
            
        time_diffs = [join_times[i+1] - join_times[i] for i in range(len(join_times)-1)]
        variance = np.var(time_diffs)
        
        if variance < 0.5:
            return min(1.0, (0.5 - variance) * 2)
        return 0
    
    def analyze_movement_patterns(self, players_list):
        movement_scores = []
        
        for player in players_list:
            if not player.is_moving():
                movement_scores.append(0.8)
                continue
                
            path_points = player.get_movement_path(30)
            if len(path_points) < 5:
                movement_scores.append(0.3)
                continue
                
            linearity = analytics.calculate_path_linearity(path_points)
            repetition = analytics.calculate_path_repetition(path_points)
            
            score = (linearity * 0.7) + (repetition * 0.3)
            movement_scores.append(score)
            
        if not movement_scores:
            return 0
            
        return sum(movement_scores) / len(movement_scores)
    
    def analyze_chat_patterns(self, players_list):
        chat_scores = []
        
        for player in players_list:
            chat_history = player.get_chat_history(50)
            
            if not chat_history:
                chat_scores.append(0.5)
                continue
                
            repetition = analytics.calculate_chat_repetition(chat_history)
            sentiment_variance = analytics.calculate_sentiment_variance(chat_history)
            response_time_consistency = analytics.calculate_response_time_consistency(chat_history)
            
            score = (repetition * 0.4) + (1 - sentiment_variance) * 0.3 + (response_time_consistency * 0.3)
            chat_scores.append(score)
            
        if not chat_scores:
            return 0
            
        return sum(chat_scores) / len(chat_scores)
    
    def analyze_username_patterns(self, players_list):
        usernames = [player.name for player in players_list]
        
        if len(usernames) < 3:
            return 0
            
        pattern_score = analytics.detect_username_patterns(usernames)
        randomness_score = analytics.calculate_username_randomness(usernames)
        
        return (pattern_score * 0.6) + (randomness_score * 0.4)
    
    def connect_to_game(self):
        game_id = self.game_id_input.get_text().strip()
        
        if not game_id:
            gui.show_notification("Error", "Please enter a valid Game ID", "error")
            return
            
        try:
            game_id = int(game_id)
        except ValueError:
            gui.show_notification("Error", "Game ID must be a number", "error")
            return
            
        self.status_label.set_text("Status: Connecting to game...")
        
        try:
            connection_result = game_service.connect_to_game(game_id)
            if connection_result.success:
                self.current_game_id = game_id
                self.is_connected = True
                self.scan_button.enable()
                game_name = game_service.get_game_name(game_id)
                self.status_label.set_text(f"Status: Connected to {game_name}")
                gui.show_notification("Success", f"Connected to {game_name}", "success")
                
                self.server_name_label.set_text(f"Server: {connection_result.server_name}")
                self.player_count_label.set_text(f"Players: {connection_result.player_count}/{connection_result.max_players}")
                self.last_scan_label.set_text("Last scan: Never")
                
                self.perform_scan()
            else:
                self.status_label.set_text(f"Status: Connection failed - {connection_result.error}")
                gui.show_notification("Error", f"Failed to connect: {connection_result.error}", "error")
        except Exception as e:
            self.status_label.set_text(f"Status: Error - {str(e)}")
            gui.show_notification("Error", f"An error occurred: {str(e)}", "error")
    
    def calculate_bot_percentage(self):
        if not self.is_connected:
            return 0, {"join_time": 0, "movement": 0, "chat": 0, "name": 0}, 0
            
        all_players = players.get_players_in_server(self.current_game_id)
        if not all_players:
            return 0, {"join_time": 0, "movement": 0, "chat": 0, "name": 0}, 0
            
        join_time_score = self.analyze_join_times(all_players)
        movement_score = self.analyze_movement_patterns(all_players)
        chat_score = self.analyze_chat_patterns(all_players)
        name_score = self.analyze_username_patterns(all_players)
        
        scores = {
            "join_time": join_time_score,
            "movement": movement_score,
            "chat": chat_score,
            "name": name_score
        }
        
        weighted_score = (
            join_time_score * 0.25 +
            movement_score * 0.35 +
            chat_score * 0.25 +
            name_score * 0.15
        )
        
        confidence = min(1.0, (len(all_players) / 10) * 0.7 + 0.3)
        
        return weighted_score * 100, scores, confidence
    
    def update_ui(self, percentage, details, confidence):
        if self.is_connected:
            server_info = game_service.get_server_info(self.current_game_id)
            player_count = players.get_player_count(self.current_game_id)
            max_players = server_info.get("max_players", 0)
            
            self.server_name_label.set_text(f"Server: {server_info.get('name', 'Unknown')}")
            self.player_count_label.set_text(f"Players: {player_count}/{max_players}")
            self.last_scan_label.set_text(f"Last scan: {datetime.now().strftime('%H:%M:%S')}")
        
        self.bot_percentage_value.set_text(f"{percentage:.1f}%")
        
        if percentage < 20:
            self.bot_percentage_value.set_color((65, 176, 230))  # Blue
        elif percentage < 50:
            self.bot_percentage_value.set_color((230, 176, 65))  # Yellow
        else:
            self.bot_percentage_value.set_color((230, 65, 65))   # Red
            
        confidence_text = "Low"
        if confidence > 0.7:
            confidence_text = "High"
        elif confidence > 0.4:
            confidence_text = "Medium"
            
        self.confidence_label.set_text(f"Detection confidence: {confidence_text}")
        
        self.progress_bar.set_value(percentage / 100)
        
        self.join_time_detail.set_text(f"Join Time Pattern: {details['join_time']*100:.1f}%")
        self.movement_detail.set_text(f"Movement Pattern: {details['movement']*100:.1f}%")
        self.chat_detail.set_text(f"Chat Pattern: {details['chat']*100:.1f}%")
        self.name_detail.set_text(f"Username Pattern: {details['name']*100:.1f}%")
        
    def perform_scan(self):
        if not self.is_connected:
            self.status_label.set_text("Status: Please connect to a game first")
            return False
            
        self.status_label.set_text("Status: Scanning server for bots...")
        
        for i in range(10):
            if not self.is_scanning and i > 0:  # Allow first scan even when not in continuous mode
                break
                
            self.progress_bar.set_value(i / 10)
            time.sleep(0.1)
            
        percentage, details, confidence = self.calculate_bot_percentage()
        self.update_ui(percentage, details, confidence)
        
        status_text = f"Status: Last scan completed at {datetime.now().strftime('%H:%M:%S')}"
        if percentage > 50:
            status_text += " - HIGH BOT PERCENTAGE DETECTED!"
        
        self.status_label.set_text(status_text)
        return percentage > 50
    
    def toggle_continuous_scan(self):
        self.is_scanning = not self.is_scanning
        
        if self.is_scanning:
            self.scan_button.set_text("Stop Scanning")
            self.continuous_scan()
        else:
            self.scan_button.set_text("Start Continuous Scanning")
    
    def continuous_scan(self):
        while self.is_scanning:
            high_bot_percentage = self.perform_scan()
            
            if high_bot_percentage:
                gui.show_notification("Warning: High Bot Percentage Detected", "This server appears to have a high number of bots.", "warning")
                
            time.sleep(self.detection_interval)
    
    def run(self):
        self.main_frame.show()
        # No immediate scan - wait for user to input game ID

if __name__ == "__main__":
    detector = BotDetectionSystem()
    detector.run()
