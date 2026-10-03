from app.security.security import SecurityManager
def main():
    security = SecurityManager()
    print("Personal AI Agent")
    print("-----------------")
    print(f"Security state: {security.get_state()}")
    security.arm()
    print(f"Security state: {security.get_state()}")
if __name__ == "__main__":
    main()