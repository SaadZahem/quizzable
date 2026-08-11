from nicegui.testing import User


async def test_index_page_welcome(user: User) -> None:
    await user.open("/")
    await user.should_see("Welcome to")
    await user.should_see("Get started")


async def test_login_page_shows_login_and_signup(user: User) -> None:
    await user.open("/login")
    await user.should_see("Log in")
    await user.should_see("Sign up")


async def test_login_page_has_username_and_password_inputs(user: User) -> None:
    await user.open("/login")
    await user.should_see("Username")
    await user.should_see("Password")
