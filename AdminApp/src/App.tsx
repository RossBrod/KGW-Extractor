import { useState, useEffect } from 'react';
import { Container, Typography, List, ListItem, Checkbox, Box, CircularProgress, Alert, Grid } from '@mui/material';
import { getPrompts, updatePromptStatus, Prompt } from './services/api';

function App() {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPrompts();
  }, []);

  const fetchPrompts = async () => {
    try {
      const data = await getPrompts();
      setPrompts(data);
      setError(null);
    } catch (error) {
      console.error('Error loading prompts:', error);
      setError('Failed to load prompts. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (functionalArea: string, currentStatus: boolean) => {
    try {
      await updatePromptStatus(functionalArea, !currentStatus);
      setPrompts(prompts.map(prompt => 
        prompt.functional_area === functionalArea ? { ...prompt, is_on: !currentStatus } : prompt
      ));
    } catch (error) {
      console.error('Error updating prompt:', error);
      setError('Failed to update prompt status. Please try again.');
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm" sx={{ py: 2 }}>
      <Box sx={{ my: 2 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Prompt Management
        </Typography>
        {prompts.length === 0 ? (
          <Typography>No prompts found.</Typography>
        ) : (
          <List sx={{ 
            '& .MuiListItem-root': {
              py: 0.5,
            }
          }}>
            {prompts.map((prompt) => (
              <ListItem key={prompt.functional_area} dense>
                <Grid container alignItems="center" spacing={1}>
                  <Grid item xs={1}>
                    <Checkbox
                      checked={prompt.is_on}
                      onChange={() => handleToggle(prompt.functional_area, prompt.is_on)}
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={11}>
                    <Typography variant="body2" sx={{ fontSize: '14px' }}>
                      {prompt.functional_area}
                    </Typography>
                  </Grid>
                </Grid>
              </ListItem>
            ))}
          </List>
        )}
      </Box>
    </Container>
  );
}

export default App;
