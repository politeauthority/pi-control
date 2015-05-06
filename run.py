if __name__ == '__main__':
    from app import app
    app.run(
	host = app.config['WEB_IP'],
        port = app.config['WEB_PORT'], 
        debug = app.config['DEBUG']
    )
