import argparse
from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.identity import Role, User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the first Mitra Solar super administrator.")
    parser.add_argument("--email", required=True, help="Administrator email address")
    parser.add_argument("--name", required=True, help="Administrator full name")
    args = parser.parse_args()

    password = getpass("New password (minimum 12 characters): ")
    confirmation = getpass("Confirm password: ")
    if len(password) < 12:
        parser.error("Password must contain at least 12 characters.")
    if password != confirmation:
        parser.error("Passwords do not match.")

    with SessionLocal() as db:
        email = args.email.strip().casefold()
        if db.scalar(select(User.id).where(User.email == email)) is not None:
            parser.error("A user with that email address already exists.")
        user = User(
            email=email,
            full_name=args.name.strip(),
            hashed_password=hash_password(password),
            role=Role.SUPER_ADMIN,
            is_active=True,
        )
        db.add(user)
        db.commit()
    print(f"Super Admin created for {email}.")


if __name__ == "__main__":
    main()
