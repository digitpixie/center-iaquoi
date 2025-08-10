import React, { useState, useEffect } from 'react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Card } from './components/ui/card';
import { Badge } from './components/ui/badge.jsx';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog';
import { Textarea } from './components/ui/textarea';
import { Alert, AlertDescription } from './components/ui/alert';
import { ArrowLeft, User, LogOut, Maximize2 } from 'lucide-react';
import './App.css';

const API_URL = 'https://491c0e54-90d7-46ea-98ce-547d638aba2d.preview.emergentagent.com';

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [tools, setTools] = useState([]);

  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ email: '', password: '', name: '' });
  const [toolFormData, setToolFormData] = useState({
    title: '',
    description: '',
    category: '',
    html_content: '',
    preview_image: ''
  });
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editingTool, setEditingTool] = useState(null);
  const [viewingTool, setViewingTool] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (user) {
      fetchTools();
    }
  }, [user]);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await fetch(`${API_URL}/api/auth/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        } else {
          localStorage.removeItem('token');
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
      }
    }
    setIsLoading(false);
  };

  const fetchTools = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/tools`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const toolsData = await response.json();
        setTools(toolsData);
      }
    } catch (error) {
      console.error('Failed to fetch tools:', error);
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const endpoint = isLoginMode ? '/api/auth/login' : '/api/auth/register';
      const payload = isLoginMode 
        ? { email: formData.email, password: formData.password }
        : { email: formData.email, password: formData.password, name: formData.name };

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        setSuccess(isLoginMode ? 'Connexion réussie!' : 'Compte créé avec succès!');
        setTimeout(() => {
          checkAuth();
          setFormData({ email: '', password: '', name: '' });
        }, 1000);
      } else {
        setError(data.detail || 'Une erreur est survenue');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setTools([]);
    setViewingTool(null);
  };

  const handleToolSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/tools/${editingTool.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(toolFormData)
      });

      if (response.ok) {
        setSuccess('Outil mis à jour!');
        fetchTools();
        setIsEditDialogOpen(false);
        setEditingTool(null);
        setToolFormData({
          title: '',
          description: '',
          category: '',
          html_content: '',
          preview_image: ''
        });
      } else {
        const data = await response.json();
        setError(data.detail || 'Erreur lors de la sauvegarde');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const openEditDialog = (tool) => {
    setEditingTool(tool);
    setToolFormData({
      title: tool.title,
      description: tool.description,
      category: tool.category,
      html_content: tool.html_content,
      preview_image: tool.preview_image || ''
    });
    setIsEditDialogOpen(true);
  };

  const openToolFullscreen = (tool) => {
    setViewingTool(tool);
  };

  const closeToolFullscreen = () => {
    setViewingTool(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  // Tool Fullscreen View
  if (viewingTool) {
    return (
      <div className="fullscreen-tool">
        <div className="fullscreen-header">
          <Button
            onClick={closeToolFullscreen}
            variant="outline"
            size="sm"
            className="bg-black/20 border-white/20 text-white hover:bg-white/10"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Button>
          <div className="flex items-center space-x-2">
            <Badge variant="secondary" className="bg-white/20 text-white border-0">
              {viewingTool.category}
            </Badge>
            <h1 className="text-white font-semibold">{viewingTool.title}</h1>
          </div>
        </div>
        <div className="fullscreen-content">
          <iframe
            srcDoc={viewingTool.html_content}
            className="w-full h-full border-0"
            title={viewingTool.title}
            sandbox="allow-scripts allow-same-origin allow-forms"
          />
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <Card className="w-full max-w-md p-8 bg-gray-900/80 backdrop-blur-sm border-gray-800 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">IA QUOI</h1>
            <p className="text-gray-400">Accédez à votre collection d'outils</p>
          </div>

          {error && (
            <Alert className="mb-4 border-red-800 bg-red-900/20">
              <AlertDescription className="text-red-200">{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="mb-4 border-green-800 bg-green-900/20">
              <AlertDescription className="text-green-200">{success}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleAuth} className="space-y-4">
            {!isLoginMode && (
              <div className="space-y-2">
                <Label htmlFor="name" className="text-gray-300">Nom</Label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required={!isLoginMode}
                  className="bg-gray-800 border-gray-700 text-white placeholder-gray-500"
                />
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-300">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
                className="bg-gray-800 border-gray-700 text-white placeholder-gray-500"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password" className="text-gray-300">Mot de passe</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
                className="bg-gray-800 border-gray-700 text-white placeholder-gray-500"
              />
            </div>

            <Button type="submit" className="w-full bg-white text-black hover:bg-gray-200">
              {isLoginMode ? 'Se connecter' : 'Créer un compte'}
            </Button>
          </form>

          <div className="text-center mt-6">
            <button
              onClick={() => setIsLoginMode(!isLoginMode)}
              className="text-gray-400 hover:text-white underline"
            >
              {isLoginMode ? 'Créer un compte' : 'Déjà un compte? Se connecter'}
            </button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <header className="bg-black/80 backdrop-blur-sm border-b border-gray-800 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <h1 className="text-xl font-bold text-white">IA QUOI</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-gray-300">
                <User className="w-4 h-4" />
                <span className="hidden sm:block">{user.name}</span>
              </div>
              <Button
                onClick={handleLogout}
                variant="outline"
                size="sm"
                className="border-gray-700 text-gray-300 hover:bg-gray-800 hover:text-white"
              >
                <LogOut className="w-4 h-4 sm:mr-2" />
                <span className="hidden sm:block">Déconnexion</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert className="mb-6 border-red-800 bg-red-900/20">
            <AlertDescription className="text-red-200">{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="mb-6 border-green-800 bg-green-900/20">
            <AlertDescription className="text-green-200">{success}</AlertDescription>
          </Alert>
        )}

        {/* Tools Grid */}
        {tools.length === 0 ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30 flex items-center justify-center">
              <span className="text-2xl">🎯</span>
            </div>
            <h3 className="text-lg font-medium text-gray-400 mb-2">
              Aucun outil pour le moment
            </h3>
            <p className="text-gray-500 mb-4">
              Aucun outil disponible pour le moment
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {tools.map((tool) => (
              <Card key={tool.id} className="tool-card group glass-card overflow-hidden flex flex-col">
                <div className="p-6 space-y-4 flex-1 flex flex-col">
                  <div>
                    <h3 className="font-semibold text-white text-base line-clamp-2 mb-2">
                      {tool.title}
                    </h3>
                  </div>
                  
                  <p className="text-sm text-gray-300 line-clamp-3 leading-relaxed flex-1">
                    {tool.description}
                  </p>
                  
                  <div className="flex flex-col space-y-3 pt-2 mt-auto">
                    <Button
                      size="sm"
                      onClick={() => openToolFullscreen(tool)}
                      className="w-full glass-button text-white font-medium shadow-lg transform transition-all duration-300 hover:scale-105"
                    >
                      <Maximize2 className="w-4 h-4 mr-2" />
                      ✨ Découvrir
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>

      {/* Edit Tool Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto bg-gray-900 border-gray-800 text-white">
          <DialogHeader>
            <DialogTitle className="text-white">Modifier l'outil</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleToolSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title" className="text-gray-300">Titre</Label>
              <Input
                id="title"
                value={toolFormData.title}
                onChange={(e) => setToolFormData({...toolFormData, title: e.target.value})}
                required
                className="bg-gray-800 border-gray-700 text-white"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="description" className="text-gray-300">Description</Label>
              <Textarea
                id="description"
                value={toolFormData.description}
                onChange={(e) => setToolFormData({...toolFormData, description: e.target.value})}
                required
                rows={3}
                className="bg-gray-800 border-gray-700 text-white"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="category" className="text-gray-300">Catégorie</Label>
              <Input
                id="category"
                value={toolFormData.category}
                onChange={(e) => setToolFormData({...toolFormData, category: e.target.value})}
                placeholder="ex: Calculateur, Analyse, Formation..."
                required
                className="bg-gray-800 border-gray-700 text-white"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="preview_image" className="text-gray-300">Image d'aperçu (URL)</Label>
              <Input
                id="preview_image"
                value={toolFormData.preview_image}
                onChange={(e) => setToolFormData({...toolFormData, preview_image: e.target.value})}
                placeholder="https://example.com/image.jpg"
                className="bg-gray-800 border-gray-700 text-white"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="html_content" className="text-gray-300">Code HTML</Label>
              <Textarea
                id="html_content"
                value={toolFormData.html_content}
                onChange={(e) => setToolFormData({...toolFormData, html_content: e.target.value})}
                required
                rows={10}
                className="font-mono text-sm bg-gray-800 border-gray-700 text-white"
                placeholder="Collez votre code HTML interactif ici..."
              />
            </div>

            <div className="flex justify-end space-x-2 pt-4">
              <Button 
                type="button" 
                variant="outline" 
                onClick={() => setIsEditDialogOpen(false)}
                className="border-gray-700 text-gray-300 hover:bg-gray-800"
              >
                Annuler
              </Button>
              <Button type="submit" className="bg-white text-black hover:bg-gray-200">
                Mettre à jour
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default App;