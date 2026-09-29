import argparse
from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.identity import Branch, Role, User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Mitra Solar portal user.")
    parser.add_argument("--email", required=True, help="Administrator email address")
    parser.add_argument("--name", required=True, help="Administrator full name")
    parser.add_argument(
        "--role",
        choices=[role.value for role in Role],
        default=Role.SUPER_ADMIN.value,
        help="Portal role (default: SUPER_ADMIN)",
    )
    parser.add_argument("--branch-id", help="Required for BRANCH users")
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
        role = Role(args.role)
        branch_id = None
        if args.branch_id:
            try:
                branch = db.get(Branch, args.branch_id)
            except (ValueError, TypeError):
                branch = None
            if branch is None or not branch.is_active:
                parser.error("--branch-id must identify an active branch.")
            branch_id = branch.id
        elif role == Role.BRANCH:
            parser.error("--branch-id is required for BRANCH users.")
        user = User(
            email=email,
            full_name=args.name.strip(),
            hashed_password=hash_password(password),
            role=role,
            branch_id=branch_id,
            is_active=True,
        )
        db.add(user)
        db.commit()
    print(f"{role.value} user created for {email}.")


if __name__ == "__main__":
    main()
