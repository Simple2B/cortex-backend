from sqlalchemy import func

from app.schemas import Client, ClientCreate
from app.models import Client as ClientDB
from app.logger import log


class ClientService:
    def register(self, **args) -> ClientDB:
        return ClientDB(
            first_name=args["first_name"] if "first_name" in args else None,
            last_name=args["last_name"] if "last_name" in args else None,
            dateBirth=args["dateBirth"] if "dateBirth" in args else None,
            address=args["address"] if "address" in args else None,
            city=args["city"] if "city" in args else None,
            state=args["state"] if "state" in args else None,
            zip=args["zip"] if "zip" in args else None,
            phone=args["phone"] if "phone" in args else None,
            email=args["email"] if "email" in args else None,
            conditions=args["conditions"] if "conditions" in args else None,
            otherLabel=args["otherLabel"] if "otherLabel" in args else None,
            checkboxesFollowing=args["checkboxesFollowing"]
            if "checkboxesFollowing" in args
            else None,
            medications=args["medications"] if "medications" in args else None,
            testedPositive=args["testedPositive"] if "testedPositive" in args else None,
            covidVaccine=args["covidVaccine"] if "covidVaccine" in args else None,
            stressfulLevel=args["stressfulLevel"] if "stressfulLevel" in args else None,
            consentMinorChild=args["consentMinorChild"]
            if "consentMinorChild" in args
            else None,
            relationshipChild=args["relationshipChild"]
            if "relationshipChild" in args
            else None,
        ).save()

    def register_new_client(self, client_data: ClientCreate) -> Client:
        client = ClientDB.query.filter(
            func.lower(ClientDB.email) == func.lower(client_data.email)
        ).first()
        if not client:
            client = self.register(**args)
            log(log.INFO, "Added client [%s]", client)
        else:
            updated = False
            first_name = (args["first_name"] if "first_name" in args else "",)
            if first_name != client.first_name:
                client.first_name = first_name
                updated = True
            last_name = (args["last_name"] if "last_name" in args else "",)
            if last_name != client.last_name:
                client.last_name = last_name
                updated = True
            # dateBirth = args["dateBirth"] if "dateBirth" in args else "",
            address = (args["address"] if "address" in args else "",)
            if address != client.address:
                client.address = address
                updated = True
            city = (args["city"] if "city" in args else "",)
            if city != client.city:
                client.city = city
                updated = True
            state = (args["state"] if "state" in args else "",)
            if state != client.state:
                client.state = state
                updated = True
            zip = (args["zip"] if "zip" in args else "",)
            if zip != client.zip:
                client.zip = zip
                updated = True
            phone = (args["phone"] if "phone" in args else "",)
            if phone != client.phone:
                client.phone = phone
                updated = True
            email = (args["email"] if "email" in args else "",)
            if email != client.email:
                client.email = email
                updated = True
            conditions = (args["conditions"] if "conditions" in args else "",)
            if conditions != client.conditions:
                client.conditions = conditions
                updated = True
            otherLabel = (args["otherLabel"] if "otherLabel" in args else "",)
            if otherLabel != client.otherLabel:
                client.otherLabel = otherLabel
                updated = True
            checkboxesFollowing = (
                args["checkboxesFollowing"] if "checkboxesFollowing" in args else "",
            )
            if checkboxesFollowing != client.checkboxesFollowing:
                client.checkboxesFollowing = checkboxesFollowing
                updated = True
            medications = (args["medications"] if "medications" in args else "",)
            if medications != client.medications:
                client.medications = medications
                updated = True
            testedPositive = (
                args["testedPositive"] if "testedPositive" in args else "",
            )
            if testedPositive != client.testedPositive:
                client.testedPositive = testedPositive
                updated = True
            covidVaccine = (args["covidVaccine"] if "covidVaccine" in args else "",)
            if covidVaccine != client.covidVaccine:
                client.covidVaccine = covidVaccine
                updated = True
            stressfulLevel = (
                args["stressfulLevel"] if "stressfulLevel" in args else "",
            )
            if stressfulLevel != client.stressfulLevel:
                client.stressfulLevel = stressfulLevel
                updated = True
            consentMinorChild = (
                args["consentMinorChild"] if "consentMinorChild" in args else "",
            )
            if consentMinorChild != client.consentMinorChild:
                client.consentMinorChild = consentMinorChild
                updated = True
            relationshipChild = (
                args["relationshipChild"] if "relationshipChild" in args else "",
            )
            if relationshipChild != client.relationshipChild:
                client.relationshipChild = relationshipChild
                updated = True

            if updated:
                client.save()

        return client
