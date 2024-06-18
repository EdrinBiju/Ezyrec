export const criteriaOptions = {
  "National Initiatives": ["NCC", "NSS"],
  "Sports & Games": ["Sports", "Games"],
  "Cultural Activities": ["Music", "Performing arts", "Literary arts"],
  "Professional Self Initiatives": [
    "Tech Fest, Tech Quiz",
    "MOOC with final assessment certificate",
    "Competitions conducted by Professional Societies",
    "Attending Full time Conference / Seminars / Exhibitions / Workshop / STTP conducted at IITs/NITs",
    "Paper presentation/publication at IITs/NITs",
    "Poster Presentation at IITs/NITs",
    "Industrial Training/Internship (at least for 5 full days)",
    "Industrial/Exhibition visits",
    "Foreign Language Skill (TOFEL/IELTS/BEC exams etc.)",
  ],
  "Entrepreneurship and Innovation": [
    "Start-up Company – Registered legally",
    "Patent-Filed",
    "Patent - Published",
    "Patent- Approved",
    "Patent- Licensed",
    "Prototype developed and tested",
    "Awards for Products developed",
    "Innovative technologies developed and used by industries/users",
    "Got venture capital funding for innovative ideas/products.",
    "Startup Employment (Offering jobs to two persons less than Rs. 15000/- per month)",
    "Societal innovations",
  ],
  "Leadership & Management": [
    "Student Professional Societies (IEEE, IET, ASME, SAE, NASA etc.)",
    "College Association Chapters (Mechanical, Civil, Electrical etc.)",
    "Festival & Technical Events (College approved)",
    "Hobby Clubs",
    "Special Initiatives (Approval from College and University is mandatory)",
    "Elected student representatives",
  ],
};

export const activityLevels = {
  "Level I": "College Events",
  "Level II": "Zonal Events",
  "Level III": "State/ University Events",
  "Level IV": "National Events",
  "Level V": "International Events",
};

// export const approvalDocuments = {
//   a: "Certificate",
//   b: "Letter from Authorities",
//   c: "Appreciation recognition letter",
//   d: "Documentary evidence",
//   e: "Legal Proof",
//   f: "Others (specify)"
// };

export const approvalDocuments = [
  {
    criteria: "National Initiatives",
    subCriteria: [
      {
        name: ["NCC", "NSS"],
        approvalDocuments: ["Certificate", "Letter from Authorities"],
      },
    ],
  },
  {
    criteria: "Sports & Games",
    subCriteria: [
      {
        name: ["Sports", "Games"],
        approvalDocuments: ["Certificate"],
      },
    ],
  },
  {
    criteria: "Cultural Activities",
    subCriteria: [
      {
        name: ["Music", "Performing arts", "Literary arts"],
        approvalDocuments: ["Certificate"],
      },
    ],
  },
  {
    criteria: "Professional Self Initiatives",
    subCriteria: [
      {
        name: [
          "Tech Fest, Tech Quiz",
          "MOOC with final assessment certificate",
          "Competitions conducted by Professional Societies",
          "Attending Full time Conference/Seminars/Exhibitions/Workshop/STTP conducted at IITs/NITs",
          "Paper presentation/publication at IITs/NITs",
          "Poster Presentation at IITs/NITs",
          "Foreign Language Skill (TOFEL/IELTS/BEC exams etc.)",
        ],
        approvalDocuments: ["Certificate", "Letter from Authorities"],
      },
      {
        name: ["Industrial Training/Internship (at least for 5 full days)"],
        approvalDocuments: ["Certificate", "Letter from Authorities"],
      },
      {
        name: ["Industrial/Exhibition visits"],
        approvalDocuments: [
          "Certificate",
          "Letter from Authorities",
          "Documentary evidence",
        ],
      },
    ],
  },
  {
    criteria: "Entrepreneurship and Innovation",
    subCriteria: [
      {
        name: [
          "Start-up Company – Registered legally",
          "Patent-Filed",
          "Patent - Published",
          "Patent- Approved",
          "Patent- Licensed",
          "Prototype developed and tested",
          "Awards for Products developed",
          "Innovative technologies developed and used by industries/users",
          "Got venture capital funding for innovative ideas/products.",
          "Startup Employment (Offering jobs to two persons less than Rs. 15000/- per month)",
          "Societal innovations",
        ],
        approvalDocuments: ["Documentary evidence"],
      },
    ],
  },
  {
    criteria: "Leadership & Management",
    subCriteria: [
      {
        name: [
          "Student Professional Societies (IEEE, IET, ASME, SAE, NASA etc.)",
          "College Association Chapters (Mechanical, Civil, Electrical etc.)",
          "Festival & Technical Events (College approved)",
          "Hobby Clubs",
          "Special Initiatives (Approval from College and University is mandatory)",
          "Elected student representatives",
        ],
        approvalDocuments: ["Documentary evidence"],
      },
    ],
  },
];

export const additionalCriteria = {
  "National Initiatives": [
    " C certificate / outstanding performance supported by certification", 
    "Best NSS Volunteer Awardee (University level), supported by certification",
    "Participation in National Integration Camp, supported by certification",
    "Pre Republic Day Parade Camp (South India), supported by certification",
    "Best NSS Volunteer Awardee (State / National level), supported by certification",
    "Participation in Republic Day Parade Camp, supported by certification",
    "International Youth Exchange Programme, supported by certification",
    "None Of The Above"
  ],
  "Sports & Games": ["Participation","First Prize", "Second Prize", "Third Prize"],
  "Cultural Activities": ["Participation","First Prize", "Second Prize", "Third Prize"],
  "Professional Self Initiatives": ["Certificate of recognition","None Of The Above"]
}