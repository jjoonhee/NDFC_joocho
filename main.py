import controller.handler as handler
import pprint

def main():
    joocho = handler.NDFC_api()
    pprint.pprint(joocho.deleteAlarms())

if __name__ == "__main__":
    main()
else:
    exit()