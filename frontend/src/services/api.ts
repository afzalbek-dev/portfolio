import axios from 'axios';
import { ServiceItem, ProjectItem, ContactRequestData, ContactRequestItem } from '../types';

const API_BASE = '/api';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchServices = async (): Promise<ServiceItem[]> => {
  const res = await api.get('/services');
  return res.data;
};

export const fetchProjects = async (category?: string): Promise<ProjectItem[]> => {
  const url = category && category !== 'all' ? `/projects?category=${category}` : '/projects';
  const res = await api.get(url);
  return res.data;
};

export const fetchVideoProjects = async () => {
  const res = await api.get('/videos');
  return res.data;
};

export const submitContactRequest = async (reqData: ContactRequestData): Promise<ContactRequestItem> => {
  const res = await api.post('/contact-requests', reqData);
  return res.data;
};

export const fetchSettings = async () => {
  const res = await api.get('/settings');
  return res.data;
};
