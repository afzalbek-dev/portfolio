export interface ServiceItem {
  id: number;
  slug: string;
  icon: string;
  title_uz: string;
  title_ru: string;
  title_en: string;
  desc_uz: string;
  desc_ru: string;
  desc_en: string;
  features_uz: string[];
  features_ru: string[];
  features_en: string[];
  price?: string;
  order_index: number;
  is_active: boolean;
}

export interface ProjectItem {
  id: number;
  category: string;
  title_uz: string;
  title_ru: string;
  title_en: string;
  desc_uz: string;
  desc_ru: string;
  desc_en: string;
  cover_image?: string;
  screenshots?: string[];
  video_url?: string;
  demo_url?: string;
  bot_url?: string;
  website_url?: string;
  github_url?: string;
  tech_stack: string[];
  is_published: boolean;
  created_at: string;
}

export interface ContactRequestData {
  name: string;
  service_id?: string;
  service_name?: string;
  description: string;
  contact_method: 'telegram' | 'whatsapp' | 'email';
  contact_value: string;
  language?: string;
  honeypot?: string;
}

export interface ContactRequestItem {
  id: number;
  name: string;
  service_id?: string;
  service_name?: string;
  description: string;
  contact_method: string;
  contact_value: string;
  language: string;
  created_at: string;
}
