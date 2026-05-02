import frappe
import json
from qyass.utils import send_mail

###
@frappe.whitelist()
def send_to_participate(*args, **kwargs):
    for value in json.loads(kwargs.get("parti")):
        doc=frappe.get_doc(value.get("participate_type"), value.get("participate"))
        msg=f"To: {doc.name} <br> Invite for meeting <br> <a href='https://qyass.newera-soft.com/meeting'>Press Here for Meeting</a>"
        msg = f"""
            To: {doc.name}
            Invite for meeting
            <a href='{doc.meeting_link}'>Press Here for Meeting</a>
            in {(json.loads(kwargs.get("obj"))).get("meeting_date")}
        """
        send_mail(doc,doc.email,msg=msg,title="Project Meeting")
    return "Meeting Link sent to participate members"


@frappe.whitelist()
def auto_save_doc(*args, **kwargs) -> None:
    "autosave the document"
    # print(kwargs.get("obj"))
    doc = frappe.get_doc(json.loads(kwargs.get("obj")))
    # print(doc)
    try:
        missing = doc._get_missing_mandatory_fields()
        for d in doc.get_all_children():
            missing.extend(d._get_missing_mandatory_fields())
        if missing:
            return 0
        doc.save()
        doc.reload()
    except Exception as e:
        print("--> ", e)
    return {"status": 1, "name": doc.get("name")}

####

@frappe.whitelist(allow_guest=True)
def get_element_data():
    query = """
        SELECT 
            vision,
            dimension,
            element,
            SUM(proof_count) AS total,
            SUM(completed_count) AS completed, 
            SUM(proof_count) - SUM(completed_count) AS `not_completed`, 
            TRUNCATE(SUM(completed_count) / NULLIF(SUM(proof_count), 0), 2) * 100 AS complete_percent
        FROM 
            `tabElements-2024`
        WHERE
            Vision = '1:الاستراتيجية والتخطيط'
        GROUP BY 
            vision, dimension, element
    """
    
    result = frappe.db.sql(query, as_dict=True)
    
    return result
