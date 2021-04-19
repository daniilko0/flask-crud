from app import create_app

app = create_app()
books = []

if __name__ == '__main__':
    app.run()
