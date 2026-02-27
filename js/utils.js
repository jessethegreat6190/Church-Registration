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
  "And my God will meet all your needs according to the riches of his glory in Christ Jesus. (Philippians 4:19)"
];

export const getWeeklyVerse = (verses = WEEKLY_VERSES) => {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  const weekIndex = Math.floor(dayOfYear / 7) % verses.length;
  return verses[weekIndex];
};

export const DEFAULT_CHURCH_PROGRAMS = {
  sunday: "8:00 AM",
  monday: "7:00 AM - 9:00 AM",
  wednesday: "Evening Glory 5pm-7pm",
  tueThu: "7:00 AM - 3:00 PM",
  friday: "3pm, 2am, 3am (Not overnight)"
};
