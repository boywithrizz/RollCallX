# RollCallX : An Attendance Management System

## Overview
This Attendance Management System is designed to help track student attendance efficiently. The system utilizes a Telegram bot for user interaction and MongoDB for data storage. It allows users to register their subjects, mark attendance, and view their attendance records.

## Features
- **User Registration**: Users can register their subjects and corresponding class schedules.
- **Attendance Marking**: Users can mark attendance for each class.
- **Attendance Tracking**: The system calculates total classes, leaves, and remaining leaves.

## Requirements
- Python 3.x
- MongoDB
- Telegram Bot API
- Required Python packages (see `requirements.txt`)

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/boywithrizz/RollCallX.git
   cd ./RollCallX
   ```
3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add your MongoDB URI and Telegram Bot Token:
   ```
   MONGODB_URI=<your-mongodb-uri>
   TELEGRAM_BOT_TOKEN_TEST=<your-telegram-bot-token>
   ```

5. **Run the Application**
   ```
   python main.py
   ```

## Usage

### Commands
- `/start`: Start the bot and get a welcome message.
- `/help`: List available commands and their usage.
- `/register`: Register your subjects with their respective schedules.
- `/markattendance`: Mark attendance for the day.
- `/showattendance`: Display attendance records for all subjects.

## Code Structure

### Main Classes
- **Universal**: Manages semester dates and exclusions.
- **Subject**: Represents a subject with its schedule and attendance data.
- **User**: Represents a user with their personal information and subject data.

### Key Functions
- `date(strdate)`: Parses date strings into date objects.
- `pdate(date)`: Formats date objects into string format.
- `f_weeklist(wlist)`: Processes the weekly list of classes.
- `num_date(semstartdate, mt3date, i)`: Generates dates for classes.
- `numdate_multi(semstartdate, mt3date, weeklist)`: Combines multiple weekly class dates into one list.
- `f_exclusions_r(list)` & `f_exclusions_l(list)`: Handle exclusion dates from classes.
- `final(totaldays, exclusions)`: Filters out excluded dates from total days.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- [Arrow](https://arrow.readthedocs.io/en/latest/) for date handling.
- [Telebot](https://github.com/eternnoir/pyTelegramBotAPI) for Telegram bot integration.
- [MongoDB](https://www.mongodb.com/) for database management.

## Developer Contact
- Authored By - Ayush Yadav
- Mail - beatscupltors@gmail.com
- LinkedIn - www.linkedin.com/in/ayush-yadav-ab0268324
