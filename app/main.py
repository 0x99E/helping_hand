import factory
import config
app = factory.create_app()

if __name__ == '__main__':
    app.run()