"""Mock data for Delhi High Court cases"""

CASE_TYPES = [
    "W.P.(C)", "CRL.A.", "FAO(OS)", "CRL.M.A.", "MAT.APP.", "CO.APP.",
    "CS(OS)", "I.A.", "CRL.REV.P.", "O.M.P.(I)", "RFA", "ARB.A."
]

FILING_YEARS = list(range(2021, 2025))

MOCK_CASES = {
    "W.P.(C).1234.2024": {
        "case_number": "1234/2024",
        "case_type": "W.P.(C)",
        "case_title": "Sunita Singh vs. Ministry of Environment",
        "petitioner_name": "Sunita Singh",
        "respondent_name": "Ministry of Environment & Ors.",
        "filing_date": "22/01/2024",
        "next_hearing_date": "18/09/2024",
        "latest_order": "The respondents are directed to file a detailed affidavit in response to the petition within four weeks. The matter concerns environmental clearance for a new project.",
        "judge_name": "Hon'ble Mr. Justice Manmohan",
        "case_status": "Pending",
        "court_hall": "Court No. 2",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_WPC_1234_2024.pdf"
    },
    "CRL.A.567.2023": {
        "case_number": "567/2023",
        "case_type": "CRL.A.",
        "case_title": "Rakesh Mehra vs. State of Delhi",
        "petitioner_name": "Rakesh Mehra",
        "respondent_name": "State of Delhi (NCT)",
        "filing_date": "15/05/2023",
        "next_hearing_date": "25/10/2024",
        "latest_order": "This is an appeal against a conviction by the trial court. The court has admitted the appeal and suspended the sentence pending further hearings. Bail has been granted.",
        "judge_name": "Hon'ble Ms. Justice Swarana Kanta Sharma",
        "case_status": "Admitted",
        "court_hall": "Court No. 31",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_CRLA_567_2023.pdf"
    },
    "FAO(OS).89.2024": {
        "case_number": "89/2024",
        "case_type": "FAO(OS)",
        "case_title": "Apex Constructions Ltd. vs. Sterling Enterprises",
        "petitioner_name": "Apex Constructions Ltd.",
        "respondent_name": "Sterling Enterprises",
        "filing_date": "02/02/2024",
        "next_hearing_date": "14/11/2024",
        "latest_order": "This first appeal from order challenges an interim injunction. After hearing arguments, the court has modified the injunction order passed by the single judge.",
        "judge_name": "Hon'ble Mr. Justice Yashwant Varma",
        "case_status": "Partially Allowed",
        "court_hall": "Court No. 9",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_FAOOS_89_2024.pdf"
    },
    "CS(OS).1121.2022": {
        "case_number": "1121/2022",
        "case_type": "CS(OS)",
        "case_title": "Innovate Pharma vs. Generic Drugs Inc.",
        "petitioner_name": "Innovate Pharma",
        "respondent_name": "Generic Drugs Inc.",
        "filing_date": "19/09/2022",
        "next_hearing_date": "03/12/2024",
        "latest_order": "This is a suit for patent infringement. The defendant has filed an application challenging the validity of the patent. Arguments on the application are to be heard.",
        "judge_name": "Hon'ble Mr. Justice C. Hari Shankar",
        "case_status": "Application Pending",
        "court_hall": "Court No. 15",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_CSOS_1121_2022.pdf"
    },
    "MAT.APP.102.2023": {
        "case_number": "102/2023",
        "case_type": "MAT.APP.",
        "case_title": "Anjali Sharma vs Varun Gupta",
        "petitioner_name": "Anjali Sharma",
        "respondent_name": "Varun Gupta",
        "filing_date": "18/04/2023",
        "next_hearing_date": "10/10/2024",
        "latest_order": "Appeal against the family court's order on maintenance. Parties have been referred to the mediation centre to attempt an amicable settlement.",
        "judge_name": "Hon'ble Ms. Justice Rekha Palli",
        "case_status": "Pending in Mediation",
        "court_hall": "Mediation Centre, Saket",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_MATAPP_102_2023.pdf"
    },
    "CRL.M.A.5567.2024": {
        "case_number": "5567/2024",
        "case_type": "CRL.M.A.",
        "case_title": "Sandeep Kumar vs State of NCT of Delhi",
        "petitioner_name": "Sandeep Kumar",
        "respondent_name": "State of NCT of Delhi",
        "filing_date": "05/02/2024",
        "next_hearing_date": "19/09/2024",
        "latest_order": "Application for anticipatory bail filed. Notice issued to the State. Investigating Officer to file a status report before the next date of hearing.",
        "judge_name": "Hon'ble Mr. Justice Amit Sharma",
        "case_status": "Notice Issued",
        "court_hall": "Court No. 14",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_CRLMA_5567_2024.pdf"
    },
    "RFA.98.2022": {
        "case_number": "98/2022",
        "case_type": "RFA",
        "case_title": "Pioneer Builders vs Capital Infraprojects",
        "petitioner_name": "Pioneer Builders",
        "respondent_name": "Capital Infraprojects",
        "filing_date": "21/07/2022",
        "next_hearing_date": "05/11/2024",
        "latest_order": "Regular First Appeal against a money decree. The parties have settled the matter and a joint compromise application has been filed. Listed for disposal.",
        "judge_name": "Hon'ble Mr. Justice V. Kameswar Rao",
        "case_status": "Settlement Pending",
        "court_hall": "Court No. 6",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_RFA_98_2022.pdf"
    },
    "ARB.A.12.2024": {
        "case_number": "12/2024",
        "case_type": "ARB.A.",
        "case_title": "Future Logistics vs National Highways Authority",
        "petitioner_name": "Future Logistics",
        "respondent_name": "National Highways Authority",
        "filing_date": "11/01/2024",
        "next_hearing_date": "22/10/2024",
        "latest_order": "Arbitration appeal challenging the award of the Arbitral Tribunal. The court has issued a notice and stayed the execution of the award subject to a deposit.",
        "judge_name": "Hon'ble Ms. Justice Prathiba M. Singh",
        "case_status": "Stay Granted",
        "court_hall": "Court No. 13",
        "pdf_link": "https://delhihighcourt.nic.in/judgments/sample_ARBA_12_2024.pdf"
    }
}
