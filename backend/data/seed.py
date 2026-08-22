from sqlalchemy.orm import Session
from backend.database import SessionLocal, Base, engine
from backend.models.concept import Concept, ConceptRelationship
from backend.models.question import Question

# We import all models to ensure Base metadata registration
from backend.models import *

def seed_data(db: Session):
    # 1. Add Concepts
    concepts_data = [
        # --- Class 1 ---
        {"id": 1, "name": "Counting", "description": "Count up to 20, write numbers, and count object sets.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Count up to 20", "Write numbers 0-20", "Match sets of objects to numbers"]},
        {"id": 2, "name": "Numbers 1-100", "description": "Read, write, and compare numbers up to 100.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Identify numbers to 100", "Compare values using greater than/less than", "Skip count by 10s"]},
        {"id": 3, "name": "Place Value Intro", "description": "Understand tens and ones.", "class_level": 1, "difficulty": "medium", "learning_objectives": ["Understand tens and ones place", "Represent numbers as groups of tens and ones"]},
        {"id": 4, "name": "Addition Intro", "description": "Adding within 20 using objects and basic formulas.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Add numbers with sum up to 20", "Solve basic word problems"]},
        {"id": 5, "name": "Subtraction Intro", "description": "Subtracting within 20 using objects and models.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Subtract numbers within 20", "Relate subtraction to addition"]},
        {"id": 6, "name": "Shapes", "description": "Identify circles, squares, triangles, and rectangles.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Identify circles, squares, triangles", "Distinguish 2D from 3D shapes"]},
        {"id": 7, "name": "Measurement", "description": "Compare length, weight, and capacity.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Compare lengths (longer/shorter)", "Compare weights (heavier/lighter)"]},
        {"id": 8, "name": "Time Intro", "description": "Tell time to the hour and half-hour.", "class_level": 1, "difficulty": "medium", "learning_objectives": ["Read clock face for hour values", "Tell time to the half-hour"]},
        {"id": 9, "name": "Money Intro", "description": "Identify pennies, nickels, dimes, quarters and bills.", "class_level": 1, "difficulty": "easy", "learning_objectives": ["Identify common coins", "Understand base coin values"]},

        # --- Class 2 ---
        {"id": 10, "name": "Numbers up to 1000", "description": "Skip count and compare values up to 1000.", "class_level": 2, "difficulty": "easy", "learning_objectives": ["Read/write numbers up to 1000", "Skip count by 5s, 10s, 100s"]},
        {"id": 11, "name": "Place Value to 1000", "description": "Identify hundreds, tens, and ones.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Identify hundreds, tens, and ones position", "Write numbers in expanded form"]},
        {"id": 12, "name": "Two-Digit Addition", "description": "Addition with regrouping.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Add 2-digit numbers with regrouping", "Explain addition using place value"]},
        {"id": 13, "name": "Two-Digit Subtraction", "description": "Subtraction with regrouping (borrowing).", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Subtract 2-digit numbers with regrouping", "Verify subtraction using addition"]},
        {"id": 14, "name": "Multiplication Intro", "description": "Repeated addition, arrays, and groups.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Understand multiplication as repeated addition", "Construct basic arrays"]},
        {"id": 15, "name": "Division Intro", "description": "Equal sharing and grouping models.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Understand partition and quotient models", "Connect division to multiplication"]},
        {"id": 16, "name": "Fractions Intro", "description": "Identify halves, thirds, and fourths.", "class_level": 2, "difficulty": "easy", "learning_objectives": ["Identify equal shares in shapes", "Name halves, thirds, fourths"]},
        {"id": 17, "name": "Shapes & Attributes", "description": "Identify sides, angles, and faces.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Count sides and angles on 2D polygons", "Identify solid shapes attributes"]},
        {"id": 18, "name": "Measurement in Standard Units", "description": "Measure in inches, feet, cm, and meters.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Estimate lengths", "Measure objects using standard tools"]},
        {"id": 19, "name": "Time to 5 Minutes", "description": "Tell time to the nearest 5 minutes.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Tell time to 5 minutes", "Differentiate AM and PM"]},
        {"id": 20, "name": "Money Operations", "description": "Solve money word problems.", "class_level": 2, "difficulty": "medium", "learning_objectives": ["Solve word problems involving money", "Find total value of coin mixtures"]},

        # --- Class 3 ---
        {"id": 21, "name": "Multiplication Mastery", "description": "Solve products within 100.", "class_level": 3, "difficulty": "medium", "learning_objectives": ["Recall basic single-digit products", "Apply commutative properties"]},
        {"id": 22, "name": "Division Mastery", "description": "Solve division problems within 100.", "class_level": 3, "difficulty": "medium", "learning_objectives": ["Solve single-digit division facts", "Identify remainders intro"]},
        {"id": 23, "name": "Fractions Concept", "description": "Numerators, denominators, and number lines.", "class_level": 3, "difficulty": "hard", "learning_objectives": ["Understand fractions as a parts-to-whole ratio", "Locate fractions on a number line"]},
        {"id": 24, "name": "Decimals Intro", "description": "Tenths place and fractional relationship.", "class_level": 3, "difficulty": "hard", "learning_objectives": ["Understand tenth fractions as decimals", "Map decimals to number line"]},
        {"id": 25, "name": "Measurement & Estimation", "description": "Estimate and measure mass, liquid volumes.", "class_level": 3, "difficulty": "medium", "learning_objectives": ["Estimate volume in liters/milliliters", "Measure mass in kilograms/grams"]},
        {"id": 26, "name": "Time Intervals", "description": "Calculate elapsed time.", "class_level": 3, "difficulty": "hard", "learning_objectives": ["Determine start/end/elapsed time", "Solve elapsed time word problems"]},
        {"id": 27, "name": "Money Word Problems", "description": "Add, subtract, and make change.", "class_level": 3, "difficulty": "medium", "learning_objectives": ["Solve multi-step money word problems", "Calculate correct change"]},
        {"id": 28, "name": "Geometry & Polygons", "description": "Quadrilaterals and geometric attributes.", "class_level": 3, "difficulty": "medium", "learning_objectives": ["Identify quadrilaterals based on side/angle rules", "Divide shapes into areas with equal parts"]},
        {"id": 29, "name": "Perimeter Intro", "description": "Measure and calculate the boundary of shapes.", "class_level": 3, "difficulty": "easy", "learning_objectives": ["Define perimeter", "Find perimeter given side measurements"]},
        {"id": 30, "name": "Data Handling", "description": "Bar graphs, pictographs, line plots.", "class_level": 3, "difficulty": "easy", "learning_objectives": ["Read and draw pictographs/bar graphs", "Solve one-step comparison graphs"]},

        # --- Class 4 ---
        {"id": 31, "name": "Large Numbers", "description": "Numbers up to 1,000,000.", "class_level": 4, "difficulty": "easy", "learning_objectives": ["Read and write numbers to 1,000,000", "Round large numbers"]},
        {"id": 32, "name": "Multi-Digit Multiplication", "description": "Multiply multi-digit by single/double digit.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Multiply up to 4-digit by 1-digit", "Multiply 2-digit by 2-digit"]},
        {"id": 33, "name": "Long Division", "description": "Divide multi-digits, interpret remainders.", "class_level": 4, "difficulty": "hard", "learning_objectives": ["Divide up to 4-digit by 1-digit", "Solve division word problems with remainders"]},
        {"id": 34, "name": "Factors", "description": "Prime, composite numbers and factor trees.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Determine all factor pairs of numbers to 100", "Identify prime and composite values"]},
        {"id": 35, "name": "Multiples", "description": "Common multiples and skip counting rules.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Find multiples of numbers 1-12", "Understand base divisibility tests"]},
        {"id": 36, "name": "Fraction Operations", "description": "Equivalent, mixed numbers, addition/subtraction.", "class_level": 4, "difficulty": "hard", "learning_objectives": ["Find equivalent fractions", "Add/subtract fractions with common denominators"]},
        {"id": 37, "name": "Decimals", "description": "Tenths, hundredths place and decimal conversion.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Write fractions with denominators 10/100 as decimals", "Compare decimals to hundredths"]},
        {"id": 38, "name": "Geometry", "description": "Lines, line segments, rays, and symmetry.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Identify parallel, perpendicular, intersecting lines", "Recognize line-symmetric figures"]},
        {"id": 39, "name": "Angles", "description": "Acute, right, obtuse, measure with protractor.", "class_level": 4, "difficulty": "hard", "learning_objectives": ["Identify acute, right, obtuse, straight angles", "Measure angles with protractor"]},
        {"id": 40, "name": "Perimeter", "description": "Perimeter formulas for rectangles/squares.", "class_level": 4, "difficulty": "easy", "learning_objectives": ["Apply perimeter formula for rectangles", "Find missing side length given perimeter"]},
        {"id": 41, "name": "Area Intro", "description": "Area formula for rectangles/squares.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Apply area formula for rectangles", "Contrast area vs perimeter"]},
        {"id": 42, "name": "Measurement", "description": "Convert units of length, mass, time.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Convert standard metric/imperial lengths", "Convert mass and time units"]},
        {"id": 43, "name": "Data Handling C4", "description": "Create and read line plots with fractions.", "class_level": 4, "difficulty": "medium", "learning_objectives": ["Construct line plots with fraction points", "Add/subtract values in line plots"]},

        # --- Class 5 ---
        {"id": 44, "name": "Large Numbers & Decimals C5", "description": "Place value systems and decimal powers.", "class_level": 5, "difficulty": "medium", "learning_objectives": ["Understand powers of ten place shifts", "Read/write decimals to thousandths"]},
        {"id": 45, "name": "Factors & Multiples GCF/LCM C5", "description": "Greatest Common Factor.", "class_level": 5, "difficulty": "medium", "learning_objectives": ["Find GCF of set of numbers", "Solve GCF word problems"]},
        {"id": 46, "name": "Lowest Common Multiple C5", "description": "LCM calculations.", "class_level": 5, "difficulty": "medium", "learning_objectives": ["Find LCM of two or more numbers", "Solve LCM word problems"]},
        {"id": 47, "name": "Fraction Multiplication/Division C5", "description": "Work with unlike denominators.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Multiply fractions by whole numbers/fractions", "Divide unit fractions by whole numbers"]},
        {"id": 48, "name": "Decimal Operations C5", "description": "Arithmetic with decimals.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Add/subtract multi-digit decimals", "Multiply and divide decimals"]},
        {"id": 49, "name": "Percentage Intro C5", "description": "Percentages as fractions of 100.", "class_level": 5, "difficulty": "medium", "learning_objectives": ["Understand percentage as base 100 fraction", "Convert fractions/decimals to percentages"]},
        {"id": 50, "name": "Geometry & Coordinates C5", "description": "Coordinate planes and polygon attributes.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Identify coordinates in quadrant 1", "Classify 2D shapes hierarchically"]},
        {"id": 51, "name": "Angles in Polygons C5", "description": "Sum of angles in triangles/quadrilaterals.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["State angle sum of triangles", "Determine missing angle sizes"]},
        {"id": 52, "name": "Complex Perimeter C5", "description": "Perimeter of composite polygons.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Deconstruct complex shapes", "Find perimeters of irregular figures"]},
        {"id": 53, "name": "Complex Area C5", "description": "Area of composite shapes.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Calculate composite polygon areas", "Apply area formulas to real-world problems"]},
        {"id": 54, "name": "Volume Intro C5", "description": "Measure volume using cubes and formulas.", "class_level": 5, "difficulty": "medium", "learning_objectives": ["Measure volume using unit cubes", "Apply volume = l x w x h"]},
        {"id": 55, "name": "Measurement Conversions C5", "description": "Multi-step conversions in metric/imperial.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Solve multi-step conversion word problems", "Interpret metric/imperial conversions"]},
        {"id": 56, "name": "Data & Representation C5", "description": "Line graphs and statistical trends.", "class_level": 5, "difficulty": "medium", "learning_objectives": ["Read line graphs showing trends", "Select appropriate graph styles"]},
        {"id": 57, "name": "Multi-step Word Problems C5", "description": "Synthesized word problems with mixed operators.", "class_level": 5, "difficulty": "hard", "learning_objectives": ["Identify required operators", "Solve multi-step word problems involving fractions/decimals"]},
    ]

    for concept in concepts_data:
        existing = db.query(Concept).filter(Concept.id == concept["id"]).first()
        if not existing:
            db.add(Concept(**concept))
    db.commit()

    # 2. Add Concept Relationships
    # source -> target
    relationships_data = [
        # Class 1 chain
        (1, 2),   # Counting -> Numbers 1-100
        (2, 3),   # Numbers 1-100 -> Place Value Intro
        (2, 4),   # Numbers 1-100 -> Addition Intro
        (4, 5),   # Addition Intro -> Subtraction Intro

        # Class 1 -> Class 2
        (2, 10),  # Numbers 1-100 (C1) -> Numbers up to 1000 (C2)
        (3, 11),  # Place Value Intro (C1) -> Place Value to 1000 (C2)
        (10, 11), # Numbers up to 1000 (C2) -> Place Value to 1000 (C2)
        (4, 12),  # Addition Intro (C1) -> Two-Digit Addition (C2)
        (11, 12), # Place Value to 1000 (C2) -> Two-Digit Addition (C2)
        (12, 13), # Two-Digit Addition (C2) -> Two-Digit Subtraction (C2)
        (12, 14), # Two-Digit Addition (C2) -> Multiplication Intro (C2)
        (14, 15), # Multiplication Intro (C2) -> Division Intro (C2)
        (15, 16), # Division Intro (C2) -> Fractions Intro (C2)
        (6, 17),  # Shapes (C1) -> Shapes & Attributes (C2)
        (7, 18),  # Measurement (C1) -> Measurement in Standard Units (C2)
        (8, 19),  # Time Intro (C1) -> Time to 5 Minutes (C2)
        (9, 20),  # Money Intro (C1) -> Money Operations (C2)

        # Class 2 -> Class 3
        (14, 21), # Multiplication Intro (C2) -> Multiplication Mastery (C3)
        (15, 22), # Division Intro (C2) -> Division Mastery (C3)
        (21, 22), # Multiplication Mastery (C3) -> Division Mastery (C3)
        (16, 23), # Fractions Intro (C2) -> Fractions Concept (C3)
        (23, 24), # Fractions Concept (C3) -> Decimals Intro (C3)
        (18, 25), # Measurement in Standard Units (C2) -> Measurement & Estimation (C3)
        (19, 26), # Time to 5 Minutes (C2) -> Time Intervals (C3)
        (20, 27), # Money Operations (C2) -> Money Word Problems (C3)
        (17, 28), # Shapes & Attributes (C2) -> Geometry & Polygons (C3)
        (12, 29), # Two-Digit Addition (C2) -> Perimeter Intro (C3)
        (10, 10), # Self-reference safeguard omitted, Numbers up to 1000 (C2) -> Data Handling (C3)
        (10, 30),

        # Class 3 -> Class 4
        (10, 31), # Numbers up to 1000 (C2) -> Large Numbers (C4)
        (21, 32), # Multiplication Mastery (C3) -> Multi-Digit Multiplication (C4)
        (22, 33), # Division Mastery (C3) -> Long Division (C4)
        (32, 33), # Multi-Digit Multiplication (C4) -> Long Division (C4)
        (21, 34), # Multiplication Mastery (C3) -> Factors (C4)
        (34, 35), # Factors (C4) -> Multiples (C4)
        (23, 36), # Fractions Concept (C3) -> Fraction Operations (C4)
        (24, 37), # Decimals Intro (C3) -> Decimals (C4)
        (28, 38), # Geometry & Polygons (C3) -> Geometry (C4)
        (38, 39), # Geometry (C4) -> Angles (C4)
        (29, 40), # Perimeter Intro (C3) -> Perimeter (C4)
        (21, 41), # Multiplication Mastery (C3) -> Area Intro (C4)
        (40, 41), # Perimeter (C4) -> Area Intro (C4)
        (25, 42), # Measurement & Estimation (C3) -> Measurement (C4)
        (30, 43), # Data Handling (C3) -> Data Handling C4

        # Class 4 -> Class 5
        (31, 44), # Large Numbers (C4) -> Large Numbers & Decimals C5
        (37, 44), # Decimals (C4) -> Large Numbers & Decimals C5
        (34, 45), # Factors (C4) -> Factors & Multiples GCF/LCM C5
        (35, 45), # Multiples (C4) -> Factors & Multiples GCF/LCM C5
        (45, 46), # GCF/LCM (C5) -> Lowest Common Multiple C5
        (36, 47), # Fraction Operations (C4) -> Fraction Multiplication/Division C5
        (46, 47), # LCM (C5) -> Fraction Multiplication/Division C5
        (37, 48), # Decimals (C4) -> Decimal Operations C5
        (44, 48), # Large Numbers & Decimals C5 -> Decimal Operations C5
        (47, 49), # Fraction Multiplication/Division C5 -> Percentage Intro C5
        (48, 49), # Decimal Operations C5 -> Percentage Intro C5
        (38, 50), # Geometry (C4) -> Geometry & Coordinates C5
        (39, 51), # Angles (C4) -> Angles in Polygons C5
        (40, 52), # Perimeter (C4) -> Complex Perimeter C5
        (41, 53), # Area Intro (C4) -> Complex Area C5
        (47, 53), # Fraction Multiplication/Division C5 -> Complex Area C5
        (41, 54), # Area Intro (C4) -> Volume Intro C5
        (42, 55), # Measurement (C4) -> Measurement Conversions C5
        (43, 56), # Data Handling C4 -> Data & Representation C5
        (47, 57), # Fraction Multiplication/Division C5 -> Multi-step Word Problems C5
        (48, 57), # Decimal Operations C5 -> Multi-step Word Problems C5
        (32, 57), # Multi-Digit Multiplication C4 -> Multi-step Word Problems C5
        (33, 57), # Long Division C4 -> Multi-step Word Problems C5
    ]

    for source_id, target_id in relationships_data:
        existing = db.query(ConceptRelationship).filter(
            ConceptRelationship.source_concept_id == source_id,
            ConceptRelationship.target_concept_id == target_id,
            ConceptRelationship.relationship_type == "prerequisite_for"
        ).first()
        if not existing:
            db.add(ConceptRelationship(
                source_concept_id=source_id,
                target_concept_id=target_id,
                relationship_type="prerequisite_for"
            ))
    db.commit()

    # 3. Add Mock Questions
    questions_data = [
        # Counting (C1)
        {
            "concept_id": 1,
            "class_level": 1,
            "difficulty": "easy",
            "question_type": "mcq",
            "question_text": "Count the stars: ⭐⭐⭐. How many are there?",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "3",
            "explanation": "If we point to each star and count them one by one, we get 1, 2, 3 stars total."
        },
        # Addition Intro (C1)
        {
            "concept_id": 4,
            "class_level": 1,
            "difficulty": "easy",
            "question_type": "mcq",
            "question_text": "What is 3 + 2?",
            "options": ["4", "5", "6", "7"],
            "correct_answer": "5",
            "explanation": "Three plus two equals five. (e.g., if you have 3 apples and get 2 more, you have 5 apples)."
        },
        # Multiplication Mastery (C3)
        {
            "concept_id": 21,
            "class_level": 3,
            "difficulty": "medium",
            "question_type": "mcq",
            "question_text": "What is 7 x 8?",
            "options": ["49", "54", "56", "64"],
            "correct_answer": "56",
            "explanation": "Seven groups of eight is equal to fifty-six (7 x 8 = 56)."
        },
        # Division Mastery (C3)
        {
            "concept_id": 22,
            "class_level": 3,
            "difficulty": "medium",
            "question_type": "mcq",
            "question_text": "What is 36 divided by 4?",
            "options": ["8", "9", "10", "12"],
            "correct_answer": "9",
            "explanation": "Since 9 x 4 = 36, then 36 divided by 4 is equal to 9."
        }
    ]

    for q in questions_data:
        # Check if the question text already exists to prevent duplicate seeding
        existing = db.query(Question).filter(Question.question_text == q["question_text"]).first()
        if not existing:
            db.add(Question(**q))
    db.commit()

if __name__ == "__main__":
    # Create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
        print("Database successfully seeded with Math syllabus and questions!")
    finally:
        db.close()
