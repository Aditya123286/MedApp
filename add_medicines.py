# add_all.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("Adding all medicines...")
    
    # Get max ID
    try:
        result = db.session.execute(db.text("SELECT MAX(id) FROM medicines"))
        max_id = result.scalar() or 0
    except:
        max_id = 0
    
    medicines = [
    # ========== PAIN RELIEF (15 medicines) ==========
    (max_id+1, "Paracetamol 500mg", "Pain reliever and fever reducer", 25, 100, "Pain Relief"),
    (max_id+2, "Diclofenac 50mg", "Anti-inflammatory painkiller", 50, 65, "Pain Relief"),
    (max_id+3, "Ibuprofen 400mg", "Pain reliever and anti-inflammatory", 35, 100, "Pain Relief"),
    (max_id+4, "Naproxen 500mg", "Long-lasting pain relief", 75, 50, "Pain Relief"),
    (max_id+5, "Aspirin 75mg", "Blood thinner and pain reliever", 40, 70, "Pain Relief"),
    (max_id+6, "Tramadol 50mg", "Strong painkiller", 85, 30, "Pain Relief"),
    (max_id+7, "Aceclofenac 100mg", "Pain and inflammation", 55, 60, "Pain Relief"),
    (max_id+8, "Piroxicam 20mg", "Anti-inflammatory", 65, 40, "Pain Relief"),
    (max_id+9, "Ketorolac 10mg", "Emergency pain relief", 45, 40, "Pain Relief"),
    (max_id+10, "Mefenamic Acid 500mg", "Pain and fever", 45, 55, "Pain Relief"),
    (max_id+11, "Nimesulide 100mg", "Pain and inflammation", 55, 50, "Pain Relief"),
    (max_id+12, "Etoricoxib 90mg", "Arthritis pain", 95, 35, "Pain Relief"),
    (max_id+13, "Celecoxib 200mg", "Rheumatoid arthritis", 120, 30, "Pain Relief"),
    (max_id+14, "Indomethacin 25mg", "Joint pain", 45, 45, "Pain Relief"),
    (max_id+15, "Meloxicam 15mg", "Osteoarthritis", 65, 40, "Pain Relief"),
    
    # ========== ANTIBIOTICS (15 medicines) ==========
    (max_id+16, "Amoxicillin 500mg", "Antibiotic for infections", 85, 50, "Antibiotics"),
    (max_id+17, "Azithromycin 500mg", "Antibiotic for respiratory", 95, 45, "Antibiotics"),
    (max_id+18, "Ciprofloxacin 500mg", "Broad spectrum antibiotic", 120, 40, "Antibiotics"),
    (max_id+19, "Ceftriaxone 1g", "Injection antibiotic", 150, 25, "Antibiotics"),
    (max_id+20, "Doxycycline 100mg", "Antibiotic for acne", 65, 55, "Antibiotics"),
    (max_id+21, "Metronidazole 400mg", "Antibiotic for infections", 45, 60, "Antibiotics"),
    (max_id+22, "Cefixime 200mg", "Antibiotic for infections", 180, 30, "Antibiotics"),
    (max_id+23, "Levofloxacin 500mg", "Antibiotic for infections", 145, 35, "Antibiotics"),
    (max_id+24, "Cefpodoxime 200mg", "Antibiotic for infections", 220, 25, "Antibiotics"),
    (max_id+25, "Amoxiclav 625mg", "Amoxicillin + Clavulanic acid", 145, 35, "Antibiotics"),
    (max_id+26, "Cefuroxime 500mg", "Antibiotic for infections", 185, 30, "Antibiotics"),
    (max_id+27, "Clarithromycin 500mg", "Macrolide antibiotic", 110, 40, "Antibiotics"),
    (max_id+28, "Norfloxacin 400mg", "UTI antibiotic", 65, 45, "Antibiotics"),
    (max_id+29, "Ofloxacin 200mg", "Antibiotic for infections", 55, 50, "Antibiotics"),
    (max_id+30, "Linezolid 600mg", "Resistant infections", 350, 20, "Antibiotics"),
    
    # ========== DIABETES (15 medicines) ==========
    (max_id+31, "Metformin 500mg", "Diabetes medication", 65, 80, "Diabetes"),
    (max_id+32, "Metformin SR 1000mg", "Diabetes medication", 95, 60, "Diabetes"),
    (max_id+33, "Glimepiride 2mg", "Blood sugar control", 65, 45, "Diabetes"),
    (max_id+34, "Glipizide 5mg", "Blood sugar control", 55, 50, "Diabetes"),
    (max_id+35, "Gliclazide 80mg", "Blood sugar control", 75, 45, "Diabetes"),
    (max_id+36, "Pioglitazone 15mg", "Diabetes medicine", 145, 30, "Diabetes"),
    (max_id+37, "Sitagliptin 100mg", "DPP-4 inhibitor", 320, 20, "Diabetes"),
    (max_id+38, "Vildagliptin 50mg", "DPP-4 inhibitor", 180, 25, "Diabetes"),
    (max_id+39, "Teneligliptin 20mg", "DPP-4 inhibitor", 165, 25, "Diabetes"),
    (max_id+40, "Dapagliflozin 10mg", "SGLT2 inhibitor", 280, 25, "Diabetes"),
    (max_id+41, "Empagliflozin 10mg", "SGLT2 inhibitor", 295, 20, "Diabetes"),
    (max_id+42, "Canagliflozin 100mg", "SGLT2 inhibitor", 270, 20, "Diabetes"),
    (max_id+43, "Insulin Human 40IU", "Short acting insulin", 350, 20, "Diabetes"),
    (max_id+44, "Insulin Glargine 100IU", "Long acting insulin", 450, 15, "Diabetes"),
    (max_id+45, "Insulin Aspart 100IU", "Rapid acting insulin", 480, 15, "Diabetes"),
    
    # ========== CARDIAC (15 medicines) ==========
    (max_id+46, "Amlodipine 5mg", "Blood pressure medication", 45, 70, "Cardiac"),
    (max_id+47, "Losartan 50mg", "Blood pressure medication", 75, 55, "Cardiac"),
    (max_id+48, "Telmisartan 40mg", "Blood pressure medication", 85, 50, "Cardiac"),
    (max_id+49, "Ramipril 5mg", "ACE inhibitor", 65, 45, "Cardiac"),
    (max_id+50, "Enalapril 5mg", "ACE inhibitor", 55, 45, "Cardiac"),
    (max_id+51, "Metoprolol 50mg", "Beta blocker", 65, 45, "Cardiac"),
    (max_id+52, "Bisoprolol 5mg", "Beta blocker", 120, 30, "Cardiac"),
    (max_id+53, "Carvedilol 6.25mg", "Beta blocker", 95, 35, "Cardiac"),
    (max_id+54, "Atorvastatin 20mg", "Cholesterol lowering", 110, 50, "Cardiac"),
    (max_id+55, "Rosuvastatin 10mg", "Cholesterol lowering", 165, 35, "Cardiac"),
    (max_id+56, "Simvastatin 20mg", "Cholesterol lowering", 95, 40, "Cardiac"),
    (max_id+57, "Clopidogrel 75mg", "Blood thinner", 145, 40, "Cardiac"),
    (max_id+58, "Aspirin 75mg Cardio", "Heart attack prevention", 35, 100, "Cardiac"),
    (max_id+59, "Furosemide 40mg", "Water pill", 25, 60, "Cardiac"),
    (max_id+60, "Spironolactone 25mg", "Water pill", 45, 50, "Cardiac"),
    
    # ========== ALLERGY (15 medicines) ==========
    (max_id+61, "Cetirizine 10mg", "Antihistamine for allergies", 45, 75, "Allergy"),
    (max_id+62, "Levocetirizine 5mg", "Antihistamine", 95, 35, "Allergy"),
    (max_id+63, "Loratadine 10mg", "Non-drowsy allergy relief", 35, 80, "Allergy"),
    (max_id+64, "Fexofenadine 120mg", "Allergy and hay fever", 85, 40, "Allergy"),
    (max_id+65, "Montelukast 10mg", "Asthma and allergy", 150, 30, "Allergy"),
    (max_id+66, "Desloratadine 5mg", "Antihistamine", 75, 40, "Allergy"),
    (max_id+67, "Bilastine 20mg", "Antihistamine", 125, 25, "Allergy"),
    (max_id+68, "Rupatadine 10mg", "Allergy medicine", 115, 25, "Allergy"),
    (max_id+69, "Hydroxyzine 25mg", "Antihistamine", 45, 45, "Allergy"),
    (max_id+70, "Promethazine 25mg", "Allergy and nausea", 25, 60, "Allergy"),
    (max_id+71, "Chlorpheniramine 4mg", "Antihistamine", 15, 80, "Allergy"),
    (max_id+72, "Pheniramine 25mg", "Anti-allergic", 20, 65, "Allergy"),
    (max_id+73, "Cyproheptadine 4mg", "Appetite stimulant", 35, 50, "Allergy"),
    (max_id+74, "Diphenhydramine 25mg", "Antihistamine", 25, 55, "Allergy"),
    (max_id+75, "Fluticasone Nasal Spray", "Nasal allergy", 185, 20, "Allergy"),
    
    # ========== GASTRO (15 medicines) ==========
    (max_id+76, "Omeprazole 20mg", "Acid reducer", 55, 90, "Gastro"),
    (max_id+77, "Pantoprazole 40mg", "Proton pump inhibitor", 95, 50, "Gastro"),
    (max_id+78, "Rabeprazole 20mg", "Acid reflux treatment", 120, 35, "Gastro"),
    (max_id+79, "Esomeprazole 40mg", "Acid reducer", 185, 25, "Gastro"),
    (max_id+80, "Lansoprazole 30mg", "Acid reducer", 135, 30, "Gastro"),
    (max_id+81, "Ranitidine 150mg", "Acid reducer", 20, 75, "Gastro"),
    (max_id+82, "Famotidine 20mg", "Acid reducer", 25, 65, "Gastro"),
    (max_id+83, "Domperidone 10mg", "Nausea and vomiting", 25, 60, "Gastro"),
    (max_id+84, "Ondansetron 4mg", "Nausea control", 35, 50, "Gastro"),
    (max_id+85, "Metoclopramide 10mg", "Nausea and vomiting", 25, 55, "Gastro"),
    (max_id+86, "Loperamide 2mg", "Anti-diarrheal", 20, 70, "Gastro"),
    (max_id+87, "Dicyclomine 10mg", "Stomach cramps", 35, 45, "Gastro"),
    (max_id+88, "Mebeverine 135mg", "Irritable bowel", 95, 35, "Gastro"),
    (max_id+89, "ORS Powder", "Oral rehydration salts", 15, 200, "Gastro"),
    (max_id+90, "Lactulose Syrup", "Constipation relief", 85, 40, "Gastro"),
    
    # ========== VITAMINS (15 medicines) ==========
    (max_id+91, "Vitamin C 500mg", "Immune support", 25, 80, "Vitamins"),
    (max_id+92, "Vitamin D3 60K", "Vitamin D supplement", 120, 60, "Vitamins"),
    (max_id+93, "Vitamin B12 1500mcg", "Energy and nerve health", 110, 45, "Vitamins"),
    (max_id+94, "Vitamin B Complex", "Vitamin B complex", 45, 60, "Vitamins"),
    (max_id+95, "Multivitamin Gold", "Daily vitamin supplement", 150, 40, "Vitamins"),
    (max_id+96, "Calcium 500mg", "Bone health", 55, 60, "Vitamins"),
    (max_id+97, "Calcium with Vitamin D3", "Bone health", 95, 55, "Vitamins"),
    (max_id+98, "Magnesium 400mg", "Muscle health", 70, 45, "Vitamins"),
    (max_id+99, "Zinc 50mg", "Immune system support", 35, 80, "Vitamins"),
    (max_id+100, "Iron 60mg", "Iron deficiency", 45, 70, "Vitamins"),
    (max_id+101, "Folic Acid 5mg", "Vitamin B9", 15, 100, "Vitamins"),
    (max_id+102, "Vitamin E 400mg", "Antioxidant", 75, 45, "Vitamins"),
    (max_id+103, "Vitamin A 10000IU", "Eye health", 55, 50, "Vitamins"),
    (max_id+104, "Biotin 10mg", "Hair and skin", 85, 40, "Vitamins"),
    (max_id+105, "Omega 3 1000mg", "Heart health", 145, 35, "Vitamins"),
    
    # ========== SKIN CARE (15 medicines) ==========
    (max_id+106, "Clotrimazole Cream", "Fungal infection", 45, 45, "Skin Care"),
    (max_id+107, "Miconazole Cream", "Fungal infection", 55, 40, "Skin Care"),
    (max_id+108, "Ketoconazole Cream", "Fungal infection", 65, 35, "Skin Care"),
    (max_id+109, "Terbinafine Cream", "Athlete's foot", 75, 30, "Skin Care"),
    (max_id+110, "Clindamycin Gel", "Acne treatment", 95, 30, "Skin Care"),
    (max_id+111, "Adapalene Gel", "Acne treatment", 125, 25, "Skin Care"),
    (max_id+112, "Tretinoin Cream", "Acne and anti-aging", 95, 25, "Skin Care"),
    (max_id+113, "Benzoyl Peroxide Gel", "Acne treatment", 65, 35, "Skin Care"),
    (max_id+114, "Hydrocortisone Cream", "Skin inflammation", 60, 40, "Skin Care"),
    (max_id+115, "Mometasone Cream", "Eczema and dermatitis", 85, 35, "Skin Care"),
    (max_id+116, "Betnovate Cream", "Skin allergies", 75, 40, "Skin Care"),
    (max_id+117, "Clobetasol Cream", "Severe skin conditions", 145, 25, "Skin Care"),
    (max_id+118, "Mupirocin Ointment", "Bacterial skin infection", 75, 35, "Skin Care"),
    (max_id+119, "Fusidic Acid Cream", "Skin infection", 85, 30, "Skin Care"),
    (max_id+120, "Silver Sulfadiazine", "Burn treatment", 95, 25, "Skin Care"),
    
    # ========== EYE CARE (15 medicines) ==========
    (max_id+121, "Moxifloxacin Eye Drops", "Eye infection", 145, 25, "Eye Care"),
    (max_id+122, "Ciprofloxacin Eye Drops", "Eye infection", 120, 25, "Eye Care"),
    (max_id+123, "Ofloxacin Eye Drops", "Eye infection", 95, 28, "Eye Care"),
    (max_id+124, "Tobramycin Eye Drops", "Eye infection", 95, 25, "Eye Care"),
    (max_id+125, "Gentamicin Eye Drops", "Eye infection", 65, 30, "Eye Care"),
    (max_id+126, "Chloramphenicol Eye", "Eye infection", 45, 35, "Eye Care"),
    (max_id+127, "Timolol Eye Drops", "Glaucoma treatment", 145, 20, "Eye Care"),
    (max_id+128, "Latanoprost Eye Drops", "Glaucoma", 185, 18, "Eye Care"),
    (max_id+129, "Brimonidine Eye Drops", "Glaucoma", 165, 18, "Eye Care"),
    (max_id+130, "Carboxymethylcellulose", "Dry eye relief", 85, 35, "Eye Care"),
    (max_id+131, "Sodium Hyaluronate", "Dry eye", 165, 20, "Eye Care"),
    (max_id+132, "Olopatadine Eye Drops", "Allergy eye drops", 185, 18, "Eye Care"),
    (max_id+133, "Ketotifen Eye Drops", "Allergy eye drops", 95, 22, "Eye Care"),
    (max_id+134, "Loteprednol Eye Drops", "Eye inflammation", 165, 15, "Eye Care"),
    (max_id+135, "Fluorometholone Eye", "Eye inflammation", 145, 20, "Eye Care"),
    
    # ========== RESPIRATORY (15 medicines) ==========
    (max_id+136, "Salbutamol Inhaler", "Asthma relief", 150, 25, "Respiratory"),
    (max_id+137, "Budesonide Inhaler", "Asthma prevention", 280, 15, "Respiratory"),
    (max_id+138, "Fluticasone Inhaler", "Asthma control", 320, 12, "Respiratory"),
    (max_id+139, "Formoterol Inhaler", "Bronchodilator", 350, 10, "Respiratory"),
    (max_id+140, "Tiotropium Inhaler", "COPD treatment", 450, 8, "Respiratory"),
    (max_id+141, "Ipratropium Inhaler", "Bronchodilator", 280, 12, "Respiratory"),
    (max_id+142, "Montelukast 10mg", "Asthma and allergy", 150, 30, "Respiratory"),
    (max_id+143, "Levosalbutamol Syrup", "Asthma for children", 65, 25, "Respiratory"),
    (max_id+144, "Acetylcysteine 600mg", "Mucus thinner", 90, 40, "Respiratory"),
    (max_id+145, "Ambroxol 30mg", "Cough expectorant", 45, 50, "Respiratory"),
    (max_id+146, "Guaifenesin 100mg", "Cough expectorant", 35, 55, "Respiratory"),
    (max_id+147, "Terbutaline 2.5mg", "Bronchodilator", 55, 35, "Respiratory"),
    (max_id+148, "Dextromethorphan Syrup", "Cough suppressant", 65, 40, "Respiratory"),
    (max_id+149, "Bromhexine 8mg", "Mucus thinner", 35, 50, "Respiratory"),
    (max_id+150, "Theophylline 400mg", "Bronchodilator", 75, 30, "Respiratory"),
    
    # ========== NEUROLOGY (15 medicines) ==========
    (max_id+151, "Gabapentin 100mg", "Neuropathic pain", 85, 35, "Neurology"),
    (max_id+152, "Gabapentin 300mg", "Neuropathic pain", 125, 30, "Neurology"),
    (max_id+153, "Pregabalin 75mg", "Neuropathic pain", 145, 25, "Neurology"),
    (max_id+154, "Pregabalin 150mg", "Neuropathic pain", 185, 20, "Neurology"),
    (max_id+155, "Carbamazepine 200mg", "Seizures", 75, 30, "Neurology"),
    (max_id+156, "Oxcarbazepine 300mg", "Seizures", 95, 25, "Neurology"),
    (max_id+157, "Valproate 500mg", "Seizures", 110, 25, "Neurology"),
    (max_id+158, "Levetiracetam 500mg", "Seizures", 165, 20, "Neurology"),
    (max_id+159, "Topiramate 50mg", "Seizures", 145, 20, "Neurology"),
    (max_id+160, "Lamotrigine 100mg", "Seizures", 135, 20, "Neurology"),
    (max_id+161, "Phenytoin 100mg", "Seizures", 45, 35, "Neurology"),
    (max_id+162, "Clonazepam 0.5mg", "Anxiety and seizures", 55, 40, "Neurology"),
    (max_id+163, "Baclofen 10mg", "Muscle relaxant", 65, 35, "Neurology"),
    (max_id+164, "Tizanidine 2mg", "Muscle relaxant", 75, 30, "Neurology"),
    (max_id+165, "Rivastigmine 3mg", "Alzheimer's", 195, 15, "Neurology"),
    
    # ========== PSYCHIATRY (15 medicines) ==========
    (max_id+166, "Escitalopram 10mg", "Antidepressant", 95, 40, "Psychiatry"),
    (max_id+167, "Sertraline 50mg", "Antidepressant", 85, 40, "Psychiatry"),
    (max_id+168, "Fluoxetine 20mg", "Antidepressant", 75, 45, "Psychiatry"),
    (max_id+169, "Paroxetine 20mg", "Antidepressant", 95, 35, "Psychiatry"),
    (max_id+170, "Citalopram 20mg", "Antidepressant", 85, 35, "Psychiatry"),
    (max_id+171, "Clonazepam 0.5mg", "Anti-anxiety", 55, 40, "Psychiatry"),
    (max_id+172, "Lorazepam 2mg", "Anti-anxiety", 65, 35, "Psychiatry"),
    (max_id+173, "Alprazolam 0.5mg", "Anti-anxiety", 45, 45, "Psychiatry"),
    (max_id+174, "Diazepam 5mg", "Anti-anxiety", 35, 50, "Psychiatry"),
    (max_id+175, "Quetiapine 25mg", "Antipsychotic", 125, 25, "Psychiatry"),
    (max_id+176, "Olanzapine 5mg", "Antipsychotic", 145, 20, "Psychiatry"),
    (max_id+177, "Risperidone 2mg", "Antipsychotic", 115, 25, "Psychiatry"),
    (max_id+178, "Haloperidol 5mg", "Antipsychotic", 45, 30, "Psychiatry"),
    (max_id+179, "Lithium 300mg", "Mood stabilizer", 65, 25, "Psychiatry"),
    (max_id+180, "Mirtazapine 15mg", "Antidepressant", 135, 20, "Psychiatry"),
    
    # ========== WOMEN HEALTH (15 medicines) ==========
    (max_id+181, "Drospirenone Ethinyl", "Birth control pill", 145, 30, "Women Health"),
    (max_id+182, "Levonorgestrel 1.5mg", "Emergency contraceptive", 95, 40, "Women Health"),
    (max_id+183, "Medroxyprogesterone", "Hormone therapy", 75, 35, "Women Health"),
    (max_id+184, "Progesterone 100mg", "Hormone therapy", 85, 30, "Women Health"),
    (max_id+185, "Clomiphene 50mg", "Fertility treatment", 165, 20, "Women Health"),
    (max_id+186, "Letrozole 2.5mg", "Fertility treatment", 145, 25, "Women Health"),
    (max_id+187, "Metformin 500mg", "PCOS treatment", 65, 50, "Women Health"),
    (max_id+188, "Dydrogesterone 10mg", "Progesterone", 125, 25, "Women Health"),
    (max_id+189, "Estradiol 2mg", "Estrogen therapy", 95, 30, "Women Health"),
    (max_id+190, "Conjugated Estrogen", "HRT", 110, 25, "Women Health"),
    (max_id+191, "Mifepristone 200mg", "Medical abortion", 250, 15, "Women Health"),
    (max_id+192, "Misoprostol 200mcg", "Medical abortion", 180, 20, "Women Health"),
    (max_id+193, "Ferrous Ascorbate", "Iron for pregnancy", 95, 40, "Women Health"),
    (max_id+194, "Calcium with Vitamin D", "Pregnancy supplement", 85, 45, "Women Health"),
    (max_id+195, "Folic Acid 5mg", "Pregnancy supplement", 15, 100, "Women Health"),
    
    # ========== MEN HEALTH (15 medicines) ==========
    (max_id+196, "Sildenafil 50mg", "Erectile dysfunction", 95, 40, "Men Health"),
    (max_id+197, "Sildenafil 100mg", "Erectile dysfunction", 145, 35, "Men Health"),
    (max_id+198, "Tadalafil 10mg", "Erectile dysfunction", 165, 30, "Men Health"),
    (max_id+199, "Tadalafil 20mg", "Erectile dysfunction", 195, 25, "Men Health"),
    (max_id+200, "Vardenafil 20mg", "Erectile dysfunction", 185, 20, "Men Health"),
    (max_id+201, "Dapoxetine 30mg", "Premature ejaculation", 125, 25, "Men Health"),
    (max_id+202, "Dapoxetine 60mg", "Premature ejaculation", 165, 20, "Men Health"),
    (max_id+203, "Finasteride 1mg", "Hair loss", 175, 30, "Men Health"),
    (max_id+204, "Finasteride 5mg", "Prostate enlargement", 195, 25, "Men Health"),
    (max_id+205, "Dutasteride 0.5mg", "Hair loss and prostate", 245, 20, "Men Health"),
    (max_id+206, "Minoxidil 5%", "Hair growth solution", 295, 20, "Men Health"),
    (max_id+207, "Minoxidil 2%", "Hair growth solution", 195, 25, "Men Health"),
    (max_id+208, "Tamsulosin 0.4mg", "Prostate", 125, 30, "Men Health"),
    (max_id+209, "Alfuzosin 10mg", "Prostate", 135, 25, "Men Health"),
    (max_id+210, "Testosterone Gel", "Testosterone therapy", 450, 10, "Men Health"),
    
    # ========== PEDIATRICS (15 medicines) ==========
    (max_id+211, "Paracetamol Syrup", "Pain and fever for children", 45, 60, "Pediatrics"),
    (max_id+212, "Ibuprofen Syrup", "Pain and fever for children", 55, 50, "Pediatrics"),
    (max_id+213, "Amoxicillin Syrup", "Antibiotic for children", 75, 45, "Pediatrics"),
    (max_id+214, "Cefpodoxime Syrup", "Antibiotic for children", 95, 35, "Pediatrics"),
    (max_id+215, "Azithromycin Syrup", "Antibiotic for children", 85, 40, "Pediatrics"),
    (max_id+216, "Montelukast Syrup", "Allergy and asthma", 95, 30, "Pediatrics"),
    (max_id+217, "Salbutamol Syrup", "Asthma for children", 65, 35, "Pediatrics"),
    (max_id+218, "Cetirizine Syrup", "Allergy for children", 45, 50, "Pediatrics"),
    (max_id+219, "Levocetirizine Syrup", "Allergy for children", 55, 45, "Pediatrics"),
    (max_id+220, "Vitamin D Drops", "Vitamin D for infants", 95, 40, "Pediatrics"),
    (max_id+221, "Iron Drops", "Iron supplement", 65, 45, "Pediatrics"),
    (max_id+222, "ORS Powder", "Dehydration", 15, 200, "Pediatrics"),
    (max_id+223, "Zinc Syrup", "Diarrhea treatment", 55, 50, "Pediatrics"),
    (max_id+224, "Multivitamin Syrup", "Vitamin supplement", 75, 45, "Pediatrics"),
    (max_id+225, "Calcium Syrup", "Bone health", 65, 40, "Pediatrics"),
    
    # ========== ONCOLOGY (15 medicines) ==========
    (max_id+226, "Tamoxifen 20mg", "Breast cancer", 350, 20, "Oncology"),
    (max_id+227, "Letrozole 2.5mg", "Breast cancer", 420, 18, "Oncology"),
    (max_id+228, "Anastrozole 1mg", "Breast cancer", 450, 15, "Oncology"),
    (max_id+229, "Imatinib 400mg", "Leukemia", 1250, 8, "Oncology"),
    (max_id+230, "Dasatinib 50mg", "Leukemia", 1850, 5, "Oncology"),
    (max_id+231, "Nilotinib 200mg", "Leukemia", 1650, 5, "Oncology"),
    (max_id+232, "Erlotinib 150mg", "Lung cancer", 1450, 6, "Oncology"),
    (max_id+233, "Gefitinib 250mg", "Lung cancer", 1350, 6, "Oncology"),
    (max_id+234, "Sorafenib 200mg", "Liver cancer", 1550, 5, "Oncology"),
    (max_id+235, "Sunitinib 50mg", "Kidney cancer", 1650, 4, "Oncology"),
    (max_id+236, "Bortezomib 3.5mg", "Multiple myeloma", 2250, 3, "Oncology"),
    (max_id+237, "Lenalidomide 25mg", "Multiple myeloma", 2850, 2, "Oncology"),
    (max_id+238, "Capecitabine 500mg", "Colon cancer", 950, 8, "Oncology"),
    (max_id+239, "5-Fluorouracil 500mg", "Colon cancer", 550, 10, "Oncology"),
    (max_id+240, "Methotrexate 15mg", "Various cancers", 350, 12, "Oncology"),
    
    # ========== VACCINES (15 medicines) ==========
    (max_id+241, "COVID-19 Vaccine", "Coronavirus vaccine", 450, 50, "Vaccines"),
    (max_id+242, "Influenza Vaccine", "Flu vaccine", 650, 40, "Vaccines"),
    (max_id+243, "Hepatitis B Vaccine", "Hepatitis B", 350, 45, "Vaccines"),
    (max_id+244, "Hepatitis A Vaccine", "Hepatitis A", 550, 35, "Vaccines"),
    (max_id+245, "MMR Vaccine", "Measles Mumps Rubella", 750, 30, "Vaccines"),
    (max_id+246, "DTaP Vaccine", "Diphtheria Tetanus Pertussis", 850, 25, "Vaccines"),
    (max_id+247, "Polio Vaccine", "Polio", 450, 40, "Vaccines"),
    (max_id+248, "HPV Vaccine", "Human Papillomavirus", 1250, 20, "Vaccines"),
    (max_id+249, "Typhoid Vaccine", "Typhoid", 550, 35, "Vaccines"),
    (max_id+250, "Chickenpox Vaccine", "Varicella", 950, 25, "Vaccines"),
    (max_id+251, "Shingles Vaccine", "Herpes zoster", 1450, 15, "Vaccines"),
    (max_id+252, "Pneumococcal Vaccine", "Pneumonia", 1150, 20, "Vaccines"),
    (max_id+253, "Meningococcal Vaccine", "Meningitis", 1250, 18, "Vaccines"),
    (max_id+254, "Rabies Vaccine", "Rabies", 850, 25, "Vaccines"),
    (max_id+255, "Tetanus Vaccine", "Tetanus", 250, 50, "Vaccines"),
    
    # ========== FIRST AID (15 medicines) ==========
    (max_id+256, "Bandages Assorted", "Various sizes", 45, 100, "First Aid"),
    (max_id+257, "Gauze Roll", "Sterile gauze", 35, 80, "First Aid"),
    (max_id+258, "Cotton Balls", "Sterile cotton", 25, 120, "First Aid"),
    (max_id+259, "Adhesive Tape", "Medical tape", 30, 90, "First Aid"),
    (max_id+260, "Antiseptic Liquid", "Dettol", 55, 60, "First Aid"),
    (max_id+261, "Betadine Solution", "Antiseptic", 65, 50, "First Aid"),
    (max_id+262, "Hydrogen Peroxide", "Wound cleaning", 35, 70, "First Aid"),
    (max_id+263, "Surgical Spirits", "Sterilization", 45, 65, "First Aid"),
    (max_id+264, "Cotton Swabs", "Ear cleaning", 20, 150, "First Aid"),
    (max_id+265, "Tweezers", "Splinter removal", 55, 40, "First Aid"),
    (max_id+266, "Scissors", "Medical scissors", 75, 35, "First Aid"),
    (max_id+267, "Gloves", "Examination gloves", 95, 50, "First Aid"),
    (max_id+268, "Masks", "Surgical masks", 85, 80, "First Aid"),
    (max_id+269, "Hand Sanitizer", "Alcohol based", 65, 70, "First Aid"),
    (max_id+270, "First Aid Kit", "Complete kit", 450, 25, "First Aid"),
    
    # ========== AYURVEDIC (15 medicines) ==========
    (max_id+271, "Chyawanprash", "Immunity booster", 195, 40, "Ayurvedic"),
    (max_id+272, "Triphala Powder", "Digestive health", 95, 45, "Ayurvedic"),
    (max_id+273, "Ashwagandha Capsules", "Stress relief", 145, 35, "Ayurvedic"),
    (max_id+274, "Brahmi Capsules", "Brain health", 165, 30, "Ayurvedic"),
    (max_id+275, "Shilajit Capsules", "Energy booster", 245, 25, "Ayurvedic"),
    (max_id+276, "Gokshura Capsules", "Sexual health", 135, 30, "Ayurvedic"),
    (max_id+277, "Tulsi Drops", "Immunity", 65, 50, "Ayurvedic"),
    (max_id+278, "Giloy Capsules", "Fever and immunity", 125, 35, "Ayurvedic"),
    (max_id+279, "Neem Capsules", "Blood purifier", 95, 40, "Ayurvedic"),
    (max_id+280, "Amla Juice", "Vitamin C rich", 115, 35, "Ayurvedic"),
    (max_id+281, "Aloe Vera Juice", "Skin and digestion", 135, 30, "Ayurvedic"),
    (max_id+282, "Karela Juice", "Diabetes control", 125, 30, "Ayurvedic"),
    (max_id+283, "Jamun Powder", "Diabetes", 85, 40, "Ayurvedic"),
    (max_id+284, "Moringa Powder", "Nutritional supplement", 95, 35, "Ayurvedic")
    ]
    
    for med in medicines:
        try:
            sql = f"INSERT INTO medicines (id, name, description, price, quantity, category) VALUES ({med[0]}, '{med[1]}', '{med[2]}', {med[3]}, {med[4]}, '{med[5]}')"
            db.session.execute(db.text(sql))
            print(f"Added: {med[1]}")
        except Exception as e:
            print(f"Error: {med[1]} - {str(e)[:50]}")
    
    db.session.commit()
    
    result = db.session.execute(db.text("SELECT COUNT(*) FROM medicines"))
    count = result.scalar()
    print(f"\nTotal medicines: {count}")
    print("DONE!")