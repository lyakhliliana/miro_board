import application

if __name__ == '__main__':
    app = application.Application()
    app.add_modules()
    app.set_bind()
    app.open_file()
    app.root.mainloop()
