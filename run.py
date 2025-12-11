from app import create_app

run_app = create_app()

if __name__ == "__main__":
    run_app.run(host="localhost", port=5555, debug=True)
