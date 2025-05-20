def switch_window(current, next_func, *args, fade=False):
    def after():
        next_func(*args)
    if fade:
        fade_out(current, after)
    else:
        current.after(100, lambda: (current.destroy(), after()))

def fade_out(win, callback, alpha=1.0):
    if alpha > 0:
        win.attributes("-alpha", alpha)
        win.after(30, lambda: fade_out(win, callback, alpha - 0.05))
    else:
        win.destroy()
        callback()