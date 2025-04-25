import axios from 'axios';

const API_URL = 'http://localhost:3000/api'; // You'll need to set up a backend API

export interface Prompt {
  functional_area: string;
  is_on: boolean;
}

export const getPrompts = async (): Promise<Prompt[]> => {
  try {
    console.log('Fetching prompts from API...');
    const response = await axios.get(`${API_URL}/prompts`);
    console.log('API response status:', response.status);
    console.log('API response data:', response.data);
    console.log('Number of prompts received:', response.data.length);
    return response.data;
  } catch (error) {
    console.error('Error fetching prompts:', error);
    if (axios.isAxiosError(error)) {
      console.error('Error response:', error.response?.data);
    }
    return [];
  }
};

export const updatePromptStatus = async (functionalArea: string, isOn: boolean): Promise<void> => {
  try {
    await axios.put(`${API_URL}/prompts/${encodeURIComponent(functionalArea)}`, { is_on: isOn });
  } catch (error) {
    console.error('Error updating prompt:', error);
    throw error;
  }
}; 