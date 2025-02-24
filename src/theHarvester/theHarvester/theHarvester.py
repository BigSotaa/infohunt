import asyncio
import platform
import multiprocessing

multiprocessing.freeze_support()

if platform.system() == "Windows":
    asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy()
else:
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        print("uvloop is not installed. Please install it using 'pip install uvloop'.")

    if "linux" in platform.system().lower():
        import aiomultiprocess

        # As we are not using Windows, we can change the spawn method to fork for greater performance
        aiomultiprocess.set_context("fork")
    asyncio.run(__main__.entry_point())
