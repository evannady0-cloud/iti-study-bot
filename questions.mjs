export const questions = [
  // --- VISUAL IQ QUESTIONS (WITH IMAGES) ---
  {
    id: 1,
    category: "Visual IQ",
    image: "matrix_arrow.png",
    question: "3x3 Matrix: The arrow rotates 45° clockwise in each step. Which arrow completes the matrix?",
    options: ["↑ (Pointing Up)", "→ (Pointing Right)", "↓ (Pointing Down)", "↖ (Pointing Top-Left)"],
    correct: 0,
    reasoning: "The arrow starts at 0° (↑) and rotates 45° clockwise at each cell: 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°. The final cell is 360° (full circle), returning to point Up ↑!"
  },
  {
    id: 2,
    category: "Visual IQ",
    image: "cube_net_1.png",
    question: "Unfolded Cube: When folded into a 3D cube, which face is OPPOSITE to face [ A ]?",
    options: ["Face B", "Face C", "Face F", "Face D"],
    correct: 2,
    reasoning: "The Golden Rule of Cubes: Any two faces with exactly ONE face between them in a straight line are opposite faces. Face A and Face F have Face C between them, so A is opposite to F!"
  },
  {
    id: 3,
    category: "Visual IQ",
    image: "domino_seq.png",
    question: "Domino Sequence: What is the next domino tile?",
    options: ["[ 5 / 1 ]", ["[ 5 / 2 ]"], ["[ 0 / 1 ]"], ["[ 4 / 6 ]"]].map(x => Array.isArray(x) ? x[0] : x),
    correct: 0,
    reasoning: "Top half increases by 1: 1, 2, 3, 4 -> 5. Bottom half increases by 1: 4, 5, 6, 0 (cycles after 6 back to 0) -> 1. Result is [ 5 / 1 ]!"
  },
  {
    id: 4,
    category: "Visual IQ",
    image: "gears_3.png",
    question: "3 Meshed Gears: Gear A rotates Clockwise (↻). In which direction will Gear C rotate?",
    options: ["Clockwise (↻)", "Counter-Clockwise (↺)", "Will not move", "Alternating"],
    correct: 0,
    reasoning: "Gear A (Clockwise) turns Gear B in opposite direction (Counter-Clockwise). Gear B turns Gear C in opposite direction (Clockwise). Rule: An odd number of meshed gears in a line (1, 3, 5) always rotate in the SAME direction as the first gear!"
  },
  {
    id: 5,
    category: "Visual IQ",
    image: "matrix_dots.png",
    question: "Dot Matrix: How many dots belong in the missing cell [ ? ]?",
    options: ["4 dots", "5 dots", "6 dots", "3 dots"],
    correct: 1,
    reasoning: "Row 1: 1, 2, 3 dots (+1 each step). Row 2: 2, 3, 4 dots (+1 each step). Row 3: 3, 4, 5 dots (+1 each step). The missing cell has 5 dots!"
  },

  // --- TEXT IQ QUESTIONS (NUMBERS & SWITCHES) ---
  {
    id: 6,
    category: "IQ - Number Series",
    question: "What number should replace the question mark?\n2, 5, 10, 17, 26, ?",
    options: ["35", "37", "36", "38"],
    correct: 1,
    reasoning: "Differences between numbers are consecutive odd numbers (+3, +5, +7, +9, +11). 26 + 11 = 37. (Alternatively: n² + 1: 1²+1, 2²+1, 3²+1, 4²+1, 5²+1, 6²+1 = 37)."
  },
  {
    id: 7,
    category: "IQ - Number Series",
    question: "What number should replace the question mark?\n5, 20, 8, 17, 11, 14, 14, ?",
    options: ["11", "12", "17", "10"],
    correct: 0,
    reasoning: "Two interleaved series! Odd positions increase by 3: 5, 8, 11, 14. Even positions decrease by 3: 20, 17, 14, (14 - 3 = 11). Next number is 11!"
  },
  {
    id: 8,
    category: "IQ - Number Series",
    question: "What number should replace the question mark?\n100, 50, 52, 26, 28, ?",
    options: ["14", "30", "16", "20"],
    correct: 0,
    reasoning: "Alternating pattern: (÷2, +2, ÷2, +2, ÷2). 100÷2=50, 50+2=52, 52÷2=26, 26+2=28. Next: 28÷2 = 14!"
  },
  {
    id: 9,
    category: "IQ - Switch Problem",
    question: "Input: [1: Red], [2: Green], [3: Blue], [4: Yellow]\nSwitch Code: (3 - 1 - 2 - 4)\nWhich color ends up in the SECOND position?",
    options: ["Red", "Green", "Blue", "Yellow"],
    correct: 0,
    reasoning: "Code (3 - 1 - 2 - 4) means: Position 1 gets element 3 (Blue), Position 2 gets element 1 (Red), Position 3 gets element 2 (Green), Position 4 gets element 4 (Yellow). The 2nd position is Red!"
  },
  {
    id: 10,
    category: "IQ - Eye Test",
    question: "Compare the two serial numbers:\n1: SN-44091-B88-Z\n2: SN-44091-B8B-Z\nAre they identical or different?",
    options: ["Identical", "Different"],
    correct: 1,
    reasoning: "Code 1 has '88' while Code 2 has '8B'. They are Different! ITI always tests 8 vs B, 1 vs I, 0 vs O."
  },

  // --- ENGLISH GRAMMAR & PREPOSITIONS ---
  {
    id: 11,
    category: "English - Prepositions",
    question: "There are 50 questions ________ this test.",
    options: ["in", "on", "at", "with"],
    correct: 1,
    reasoning: "Fixed English expression: questions ON a test / ON an exam (questions are printed on the surface of the paper/test). Never 'in this test'!"
  },
  {
    id: 12,
    category: "English - Prepositions",
    question: "She usually prefers drinking tea ________ coffee.",
    options: ["than", "to", "over", "from"],
    correct: 1,
    reasoning: "The verb PREFER always takes 'TO' (Prefer X to Y). We only use 'than' with 'would rather'!"
  },
  {
    id: 13,
    category: "English - Grammar",
    question: "We are really looking forward to ________ you at the interview.",
    options: ["meet", "meeting", "met", "be met"],
    correct: 1,
    reasoning: "Famous ITI trap! In the idiom 'look forward to', 'to' is a preposition, so it must be followed by a gerund [Verb + ING] ➔ looking forward to meeting you!"
  },
  {
    id: 14,
    category: "English - Grammar",
    question: "If I ________ enough money, I would buy a new laptop.",
    options: ["have", "had", "has", "will have"],
    correct: 1,
    reasoning: "Second Conditional (Unreal Present): If + Past Simple (had), would + infinitive (would buy)."
  },
  {
    id: 15,
    category: "English - Grammar",
    question: "Tomorrow is a national holiday. We ________ wake up early.",
    options: ["mustn't", "don't have to", "couldn't", "aren't"],
    correct: 1,
    reasoning: "Lack of necessity: 'don't have to' means it's not required. 'Mustn't' means strictly forbidden by law."
  },

  // --- ENGLISH SITUATIONAL EXPRESSIONS ---
  {
    id: 16,
    category: "English - Situational",
    question: "You are going to be late home because you are going to watch the school play. So you phone home and say:",
    options: [
      "I'm sorry that I was late yesterday.",
      "Hello Mum! I thought I'd let you know I'll be a couple of hours late.",
      "Why are you calling me right now?",
      "Don't cook dinner tomorrow."
    ],
    correct: 1,
    reasoning: "Polite advance notice: 'I thought I'd let you know...' is the standard polite way to inform family about future delay."
  },
  {
    id: 17,
    category: "English - Situational",
    question: "A friend has bought a new skirt. The style and colour really suit her. What do you say?",
    options: [
      "That skirt looks perfect on you. You look lovely in it!",
      "Why did you waste your salary on that?",
      "I have a much nicer skirt at home.",
      "You should never wear that color again."
    ],
    correct: 0,
    reasoning: "A polite, encouraging compliment matching the situation."
  },
  {
    id: 18,
    category: "English - Situational",
    question: "You are a stranger in town and want to visit a museum. You stop someone and say:",
    options: [
      "Where is the museum? Take me there now!",
      "Excuse me. Could you tell me the way to the archaeological museum?",
      "I hate this town, where is the building?",
      "Do you work at the museum?"
    ],
    correct: 1,
    reasoning: "Polite inquiry: Starts with 'Excuse me' and uses modal 'Could you tell me...'"
  },

  // --- ENGLISH VOCABULARY ---
  {
    id: 19,
    category: "English - Vocabulary",
    question: "What is the closest synonym for the word 'CRUCIAL'?",
    options: ["Optional", "Vital", "Minor", "Rare"],
    correct: 1,
    reasoning: "Crucial = Vital = Essential = Extremely important. Minor is the opposite!"
  },
  {
    id: 20,
    category: "English - Vocabulary",
    question: "He admits ________ that he is a bit of a womanizer.",
    options: ["awkwardly", "unabashedly", "secretly", "politely"],
    correct: 1,
    reasoning: "Unabashedly = without shame or embarrassment (بلا خجل)."
  }
];
