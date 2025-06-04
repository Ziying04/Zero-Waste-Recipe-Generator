# Zero-Waste Recipe Generator 🥗♻️

A Django-based platform that leverages AI to generate recipes from ingredients you already have, helps track expiring food items, and enables community food sharing to reduce food waste.

![Zero Waste Banner](./assets/images/banner.png)

## 🌟 Features

- **AI Recipe Generator**: Get creative recipes based on ingredients you have on hand
- **Expiration Tracker**: Track food items in your pantry and receive notifications before they expire
- **Community Food Sharing**: Share excess food with your local community
- **User Profiles**: Save favorite recipes, track your waste reduction impact
- **Sustainable Tips**: Learn tips and tricks for reducing food waste

## 🔧 Technologies

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **AI Integration**: OpenAI API for recipe generation
- **Authentication**: Django Auth

## 📋 Prerequisites

- Python 3.8+
- Django 3.2+
- PostgreSQL
- OpenAI API key

## 🚀 Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Zero-Waste-Recipe-Generator.git
   cd Zero-Waste-Recipe-Generator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key and database configuration:
     ```
     OPENAI_API_KEY=your_api_key
     DB_NAME=your_db_name
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_HOST=localhost
     ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## 📱 Usage

1. **Register/Login**: Create an account or login to your existing account
2. **Add Ingredients**: Input ingredients you have in your pantry
3. **Generate Recipes**: Get AI-generated recipes based on your available ingredients
4. **Track Expiration**: Add expiration dates to your food items and receive notifications
5. **Share Food**: List excess food items for community sharing

## 💡 How It Works

![How It Works](./assets/images/how_it_works.png)

1. **Input Ingredients**: Enter whatever ingredients you have available
2. **AI Processing**: Our AI analyzes your ingredients and generates suitable recipes
3. **Reduce Waste**: Cook with what you have instead of buying more ingredients
4. **Track & Share**: Keep track of what's expiring soon and share what you can't use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Project Link: [https://github.com/yourusername/Zero-Waste-Recipe-Generator](https://github.com/yourusername/Zero-Waste-Recipe-Generator)

## 🙏 Acknowledgments

- OpenAI for providing the API for recipe generation
- All contributors who have helped build this project
- The sustainable food community for inspiration
