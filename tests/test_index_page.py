from nicegui.testing import User


async def test_brand(user: User) -> None:
    await user.open("/")
    await user.should_see("Quizzable")
