from relateiq.client import RelateIQ
from relateiq.contacts import Contact

RelateIQ("55520a2ce4b05a63141d0c4d", "kLwfqJEshUeGt5iFwMyj48GOnfV")
contact = Contact()
contact.name("James McSales")
contact.email(["james.mcsales@relateiq.com","jimmy@personal.com"])
contact.phone(["(888) 555-1234","(888) 555-0000"])
contact.address("123 Main St, USA")
contact.company("RelateIQ")
contact.title("Noob")
contact.twhan("@jamesmcsales")
contact.create()