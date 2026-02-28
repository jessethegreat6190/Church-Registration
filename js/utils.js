// Utility functions for Church Registration application

export const formatName = (name) => {
  return name.toLowerCase()
    .split(' ')
    .filter(word => word.length > 0)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

export const isUpcomingBirthday = (month, day) => {
  if (!month || !day) return false;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const bdayThisYear = new Date(today.getFullYear(), month - 1, day);
  if (bdayThisYear < today) {
    bdayThisYear.setFullYear(today.getFullYear() + 1);
  }
  
  const diffTime = bdayThisYear - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays <= 7 && diffDays >= 0;
};

export const getDaysUntilBirthday = (month, day) => {
  if (!month || !day) return null;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const bdayThisYear = new Date(today.getFullYear(), month - 1, day);
  if (bdayThisYear < today) {
    bdayThisYear.setFullYear(today.getFullYear() + 1);
  }
  
  const diffTime = bdayThisYear - today;
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

export const formatBirthday = (month, day) => {
  if (!month || !day) return "—";
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return `${day} ${monthNames[month - 1]}`;
};

export const WEEKLY_VERSES = [
  "The Lord bless you and keep you; the Lord make his face shine on you and be gracious to you. (Numbers 6:24-25)",
  "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you. (Jeremiah 29:11)",
  "The Lord is my shepherd; I shall not want. He makes me lie down in green pastures. (Psalm 23:1-2)",
  "Trust in the Lord with all your heart and lean not on your own understanding. (Proverbs 3:5)",
  "But those who hope in the Lord will renew their strength. They will soar on wings like eagles. (Isaiah 40:31)",
  "The Lord your God is with you, the Mighty Warrior who saves. He will take great delight in you. (Zephaniah 3:17)",
  "I can do all this through him who gives me strength. (Philippians 4:13)",
  "And my God will meet all your needs according to the riches of his glory in Christ Jesus. (Philippians 4:19)",
  "Fear not, for I am with you; be not dismayed, for I am your God. I will strengthen you and help you. (Isaiah 41:10)",
  "The Lord will fight for you; you need only to be still. (Exodus 14:14)",
  "Ask and it will be given to you; seek and you will find; knock and the door will be opened to you. (Matthew 7:7)",
  "Cast all your anxiety on him because he cares for you. (1 Peter 5:7)",
  "The peace of God, which transcends all understanding, will guard your hearts and your minds. (Philippians 4:7)",
  "Commit to the Lord whatever you do, and he will establish your plans. (Proverbs 16:3)",
  "The Lord is good, a refuge in times of trouble. He cares for those who trust in him. (Nahum 1:7)",
  "Draw near to God and He will draw near to you. (James 4:8)",
  "The Lord is my light and my salvation—whom shall I fear? (Psalm 27:1)",
  "He gives strength to the weary and increases the power of the weak. (Isaiah 40:29)",
  "Delight yourself in the Lord, and he will give you the desires of your heart. (Psalm 37:4)",
  "The name of the Lord is a fortified tower; the righteous run to it and are safe. (Proverbs 18:10)",
  "Give thanks to the Lord, for he is good; his love endures forever. (Psalm 107:1)",
  "I will never leave you nor forsake you. (Hebrews 13:5)",
  "The Lord is close to the brokenhearted and saves those who are crushed in spirit. (Psalm 34:18)",
  "In all these things we are more than conquerors through him who loved us. (Romans 8:37)",
  "But seek first his kingdom and his righteousness, and all these things will be given to you as well. (Matthew 6:33)",
  "Everything is possible for one who believes. (Mark 9:23)",
  "He restores my soul. He leads me in paths of righteousness for his name's sake. (Psalm 23:3)",
  "God is our refuge and strength, an ever-present help in trouble. (Psalm 46:1)",
  "The Lord is faithful, and he will strengthen you and protect you from the evil one. (2 Thessalonians 3:3)",
  "The joy of the Lord is your strength. (Nehemiah 8:10)",
  "Blessed is the one who trusts in the Lord, whose confidence is in him. (Jeremiah 17:7)",
  "Therefore, if anyone is in Christ, the new creation has come: The old has gone, the new is here! (2 Corinthians 5:17)",
  "Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up. (Galatians 6:9)",
  "Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go. (Joshua 1:9)",
  "God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. (John 3:16)",
  "The Lord is my strength and my shield; my heart trusts in him, and he helps me. (Psalm 28:7)"
];

export const getWeeklyVerse = (verses = WEEKLY_VERSES) => {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  // Updates every two days (Day 1: 0, Day 2-3: 1, Day 4-5: 2...)
  const index = Math.floor(dayOfYear / 2) % verses.length;
  return verses[index];
};

export const DEFAULT_CHURCH_PROGRAMS = {
  sunday: "8:00 AM",
  monday: "7:00 AM - 9:00 AM",
  wednesday: "Evening Glory 5pm-7pm",
  tueThu: "7:00 AM - 3:00 PM",
  friday: "3pm, 2am, 3am (Not overnight)"
};
