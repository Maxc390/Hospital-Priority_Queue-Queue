import pygame
import sys

class InputBox:
    def __init__(self, x, y, w, h, label, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.label = label
        self.font = pygame.font.Font(None, 36)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Add the functionality to handle the entered text
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        width = max(200, self.font.size(self.text)[0] + 10)
        self.rect.w = width

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width()+10)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        label = self.font.render(self.label, True, (0, 0, 0))
        screen.blit(label, (self.rect.x - 100, self.rect.y + 5))

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def calculate_priority(self, age, text):
        if age >= 55:
            return 2
        elif text == "critical":
            return 0
        elif text in ["investor", "politician"]:
            return 1
        else:
            return len(self.elements) + 1

    def add(self, name, age, text):
        if age:
            age = int(age)
        else:
            age = 0  # Default age if not provided
        priority = self.calculate_priority(age, text)

        entry = {"name": name, "age": age, "priority": priority}
        self.elements.append(entry)
        self.elements.sort(key=lambda x: x["priority"], reverse=True)

    def update_person(self, name, age, new_text):
        # Find the person with the given name and age
        person_index = next((index for (index, person) in enumerate(self.elements) if person["name"] == name and person["age"] == age), None)
        if person_index is not None:
            # Remove the old person
            old_person = self.elements.pop(person_index)
            # Calculate the new priority
            new_priority = self.calculate_priority(age, new_text)
            # Add the updated person with the new priority
            updated_person = {"name": name, "age": age, "priority": new_priority}
            self.elements.append(updated_person)
            self.elements.sort(key=lambda x: x["priority"], reverse=True)
            return f"Updated person: {old_person} -> {updated_person}"
        else:
            return f"Person not found: {name}, {age}"

    def delete_person(self, name, age):
        # Find the person with the given name and age
        person_index = next((index for (index, person) in enumerate(self.elements) if person["name"] == name and person["age"] == age), None)
        if person_index is not None:
            # Remove the person
            deleted_person = self.elements.pop(person_index)
            return f"Deleted person: {deleted_person}"
        else:
            return f"Person not found: {name}, {age}"

    def min(self):
        if not self.is_empty():
            return self.elements[-1]

    def remove_min(self):
        if not self.is_empty():
            return self.elements.pop()

    def is_empty(self):
        return len(self.elements) == 0

    def length(self):
        return len(self.elements)

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Priority Queue Visualization")

# Load and resize the image
hospital_image = pygame.image.load("Hospital.png")
hospital_image = pygame.transform.scale(hospital_image, (WIDTH // 2, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)

# Priority queue
priority_queue = PriorityQueue()

# Entry boxes
name_box = InputBox(560, 10, 200, 30, "Name")
age_box = InputBox(560, 50, 200, 30, "Age")
text_box = InputBox(560, 90, 200, 30, "Priority")
input_boxes = [name_box, age_box, text_box]

# Buttons
add_button = pygame.Rect(600, 130, 160, 50)
min_button = pygame.Rect(400, 130, 160, 50)
remove_min_button = pygame.Rect(600, 190, 160, 50)
is_empty_button = pygame.Rect(400, 190, 160, 50)
length_button = pygame.Rect(600, 250, 160, 50)
update_button = pygame.Rect(400, 250, 160, 50)
delete_button = pygame.Rect(600, 310, 160, 50)

buttons = [add_button, min_button, remove_min_button, is_empty_button, length_button, update_button, delete_button]

# Text display variables
text_display = ""
text_display_font = pygame.font.Font(None, 28)
text_display_color = BLACK
text_display_position = (10, 10)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if any button is clicked
            for i, button in enumerate(buttons):
                if button.collidepoint(mouse_pos):
                    if i == 0:  # Add button
                        # Add the functionality to handle the entered text
                        print("Add button clicked")
                        priority_queue.add(
                            name_box.text.strip(),
                            int(age_box.text.strip()),
                            text_box.text.strip()
                        )
                        for box in input_boxes:
                            box.text = ''  # Clear text inputs
                        text_display = "Person added successfully"
                    elif i == 1:  # Min button
                        text_display = f"Min: {priority_queue.min()}"
                    elif i == 2:  # Remove Min button
                        text_display = f"Removed Min: {priority_queue.remove_min()}"
                    elif i == 3:  # Is Empty button
                        text_display = f"Is Empty: {priority_queue.is_empty()}"
                    elif i == 4:  # Length button
                        text_display = f"Length: {priority_queue.length()}"
                    elif i == 5:  # Update button
                        text_display = priority_queue.update_person(name_box.text.strip(), int(age_box.text.strip()), text_box.text.strip())
                        for box in input_boxes:
                            box.text = ''  # Clear text inputs
                    elif i == 6:  # Delete button
                        text_display = priority_queue.delete_person(name_box.text.strip(), int(age_box.text.strip()))
                        for box in input_boxes:
                            box.text = ''  # Clear text inputs

    # Draw entry boxes
    for box in input_boxes:
        box.update()

    # Draw buttons
    for button in buttons:
        pygame.draw.rect(screen, RED, button)

    # Draw text on buttons
    add_text = font.render("Add", True, BLACK)
    min_text = font.render("Min", True, BLACK)
    remove_min_text = font.render("Remove Min", True, BLACK)
    is_empty_text = font.render("Is Empty", True, BLACK)
    length_text = font.render("Length", True, BLACK)
    update_text = font.render("Update", True, BLACK)
    delete_text = font.render("Delete", True, BLACK)

    # Draw the components on the screen
    screen.fill(WHITE)
    for box in input_boxes:
        box.draw(screen)

    for button in buttons:
        pygame.draw.rect(screen, RED, button)

    screen.blit(add_text, (add_button.x + 25, add_button.y + 15))
    screen.blit(min_text, (min_button.x + 25, min_button.y + 15))
    screen.blit(remove_min_text, (remove_min_button.x + 15, remove_min_button.y + 15))
    screen.blit(is_empty_text, (is_empty_button.x + 15, is_empty_button.y + 15))
    screen.blit(length_text, (length_button.x + 15, length_button.y + 15))
    screen.blit(update_text, (update_button.x + 15, update_button.y + 15))
    screen.blit(delete_text, (delete_button.x + 15, delete_button.y + 15))

    # Draw the image on the screen
    screen.blit(hospital_image, (0, 0))

    # Draw the text display
    text_surface = text_display_font.render(text_display, True, text_display_color)
    screen.blit(text_surface, text_display_position)

    # Draw the images and text for each element in the priority queue
    image_width, image_height = 50, 50
    distance_between_images = 70
    start_x = 150
    start_y = 520
    for i, person in enumerate(reversed(priority_queue.elements)):
        image_rect = pygame.Rect(start_x + i * distance_between_images, start_y, image_width, image_height)
        patient_image = pygame.image.load("Patient.png")
        patient_image = pygame.transform.scale(patient_image, (image_width, image_height))
        screen.blit(patient_image, image_rect)
        
        text_surface = small_font.render(f"{person['name']} ({person['age']})", True, RED)
        screen.blit(text_surface, (image_rect.x-30, image_rect.y - 20))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
