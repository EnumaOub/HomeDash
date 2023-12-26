from dashboard.main import app
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

server = app.server
if __name__ == "__main__":
    print()
    app.run_server(debug=True)