#Quizzard

**It is a simple quiz application** created using Bootstrap and Django.

## To run the Quizzard backend locally:

1. Ensure that you have Python 3.x and pip installed on your system.
2. Clone this repository using the following command:
   ```
   git clone https://github.com/rsk-2002/brainbunny-backend-django.git
   ```
3. Create a virtual environment:
   ```
   python3 -m venv env
   ```
   OR
   ```
   python -m virtualenv env
   ```
4. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source env/bin/activate
     ```
   - On Windows:
     ```
     env\Scripts\activate
     ```
5. Install the project dependencies:
   ```
   pip install -r requirement.txt
   ```
6. Apply the database migrations:
   ```
   python manage.py migrate
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```

## Contributors

> Rudra Narayan Sahoo
> Rounak Biswal
> Sanjana Mohanta

## Contributing

Contributions are welcome! If you encounter any issues or have ideas for improvements, please open an issue or submit a pull request.

## License

[MIT](https://choosealicense.com/licenses/mit/)
