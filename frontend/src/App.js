import React, { useState, useEffect } from 'react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Card } from './components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';
import { Textarea } from './components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Badge } from './components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Alert, AlertDescription } from './components/ui/alert';
import { Eye, Plus, Edit, Trash2, BookOpen, Wrench, Calculator, BarChart3, User, LogOut } from 'lucide-react';
import './App.css';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [tools, setTools] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ email: '', password: '', name: '' });
  const [toolFormData, setToolFormData] = useState({
    title: '',
    description: '',
    category: '',
    html_content: '',
    preview_image: ''
  });
  const [isToolDialogOpen, setIsToolDialogOpen] = useState(false);
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
      fetchCategories();
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

  const fetchCategories = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/categories`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const categoriesData = await response.json();
        setCategories(categoriesData);
      }
    } catch (error) {
      console.error('Failed to fetch categories:', error);
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
    setCategories([]);
  };

  const handleToolSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');
      const method = editingTool ? 'PUT' : 'POST';
      const url = editingTool 
        ? `${API_URL}/api/tools/${editingTool.id}`
        : `${API_URL}/api/tools`;

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(toolFormData)
      });

      if (response.ok) {
        setSuccess(editingTool ? 'Outil mis à jour!' : 'Outil créé!');
        fetchTools();
        fetchCategories();
        setIsToolDialogOpen(false);
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

  const handleDeleteTool = async (toolId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet outil?')) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/tools/${toolId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.ok) {
        setSuccess('Outil supprimé!');
        fetchTools();
        fetchCategories();
      } else {
        setError('Erreur lors de la suppression');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const openToolDialog = (tool = null) => {
    if (tool) {
      setEditingTool(tool);
      setToolFormData({
        title: tool.title,
        description: tool.description,
        category: tool.category,
        html_content: tool.html_content,
        preview_image: tool.preview_image || ''
      });
    } else {
      setEditingTool(null);
      setToolFormData({
        title: '',
        description: '',
        category: '',
        html_content: '',
        preview_image: ''
      });
    }
    setIsToolDialogOpen(true);
  };

  const filteredTools = selectedCategory === 'all' 
    ? tools 
    : tools.filter(tool => tool.category === selectedCategory);

  const getCategoryIcon = (category) => {
    switch (category.toLowerCase()) {
      case 'calculateur': return <Calculator className="w-4 h-4" />;
      case 'analyse': return <BarChart3 className="w-4 h-4" />;
      case 'formation': return <BookOpen className="w-4 h-4" />;
      default: return <Wrench className="w-4 h-4" />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-slate-800"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
        <Card className="w-full max-w-md p-8 bg-white/80 backdrop-blur-sm border-0 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Outils Interactifs</h1>
            <p className="text-slate-600">Accédez à votre collection d'outils</p>
          </div>

          {error && (
            <Alert className="mb-4 border-red-200 bg-red-50">
              <AlertDescription className="text-red-800">{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="mb-4 border-green-200 bg-green-50">
              <AlertDescription className="text-green-800">{success}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleAuth} className="space-y-4">
            {!isLoginMode && (
              <div className="space-y-2">
                <Label htmlFor="name">Nom</Label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required={!isLoginMode}
                  className="bg-white/50"
                />
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
                className="bg-white/50"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">Mot de passe</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
                className="bg-white/50"
              />
            </div>

            <Button type="submit" className="w-full bg-slate-800 hover:bg-slate-700">
              {isLoginMode ? 'Se connecter' : 'Créer un compte'}
            </Button>
          </form>

          <div className="text-center mt-6">
            <button
              onClick={() => setIsLoginMode(!isLoginMode)}
              className="text-slate-600 hover:text-slate-800 underline"
            >
              {isLoginMode ? 'Créer un compte' : 'Déjà un compte? Se connecter'}
            </button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Tool className="w-8 h-8 text-slate-800" />
              <h1 className="text-xl font-bold text-slate-800">Outils Interactifs</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-slate-600">
                <User className="w-4 h-4" />
                <span>{user.name}</span>
              </div>
              <Button
                onClick={handleLogout}
                variant="outline"
                size="sm"
                className="border-slate-300 hover:bg-slate-100"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Déconnexion
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertDescription className="text-red-800">{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="mb-6 border-green-200 bg-green-50">
            <AlertDescription className="text-green-800">{success}</AlertDescription>
          </Alert>
        )}

        {/* Filters and Add Button */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 space-y-4 sm:space-y-0">
          <div className="flex flex-wrap items-center gap-2">
            <Button
              variant={selectedCategory === 'all' ? 'default' : 'outline'}
              onClick={() => setSelectedCategory('all')}
              className={selectedCategory === 'all' ? 'bg-slate-800 hover:bg-slate-700' : ''}
            >
              Tous ({tools.length})
            </Button>
            {categories.map((category) => (
              <Button
                key={category.name}
                variant={selectedCategory === category.name ? 'default' : 'outline'}
                onClick={() => setSelectedCategory(category.name)}
                className={`flex items-center space-x-1 ${
                  selectedCategory === category.name ? 'bg-slate-800 hover:bg-slate-700' : ''
                }`}
              >
                {getCategoryIcon(category.name)}
                <span>{category.name} ({category.count})</span>
              </Button>
            ))}
          </div>

          <Dialog open={isToolDialogOpen} onOpenChange={setIsToolDialogOpen}>
            <DialogTrigger asChild>
              <Button 
                onClick={() => openToolDialog()}
                className="bg-slate-800 hover:bg-slate-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Ajouter un outil
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>
                  {editingTool ? 'Modifier l\'outil' : 'Ajouter un nouvel outil'}
                </DialogTitle>
              </DialogHeader>
              <form onSubmit={handleToolSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Titre</Label>
                  <Input
                    id="title"
                    value={toolFormData.title}
                    onChange={(e) => setToolFormData({...toolFormData, title: e.target.value})}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={toolFormData.description}
                    onChange={(e) => setToolFormData({...toolFormData, description: e.target.value})}
                    required
                    rows={3}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="category">Catégorie</Label>
                  <Input
                    id="category"
                    value={toolFormData.category}
                    onChange={(e) => setToolFormData({...toolFormData, category: e.target.value})}
                    placeholder="ex: Calculateur, Analyse, Formation..."
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="preview_image">Image d'aperçu (URL)</Label>
                  <Input
                    id="preview_image"
                    value={toolFormData.preview_image}
                    onChange={(e) => setToolFormData({...toolFormData, preview_image: e.target.value})}
                    placeholder="https://example.com/image.jpg"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="html_content">Code HTML</Label>
                  <Textarea
                    id="html_content"
                    value={toolFormData.html_content}
                    onChange={(e) => setToolFormData({...toolFormData, html_content: e.target.value})}
                    required
                    rows={10}
                    className="font-mono text-sm"
                    placeholder="Collez votre code HTML interactif ici..."
                  />
                </div>

                <div className="flex justify-end space-x-2 pt-4">
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={() => setIsToolDialogOpen(false)}
                  >
                    Annuler
                  </Button>
                  <Button type="submit" className="bg-slate-800 hover:bg-slate-700">
                    {editingTool ? 'Mettre à jour' : 'Créer'}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Tools Grid */}
        {filteredTools.length === 0 ? (
          <div className="text-center py-12">
            <Tool className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-600 mb-2">
              {selectedCategory === 'all' ? 'Aucun outil pour le moment' : `Aucun outil dans "${selectedCategory}"`}
            </h3>
            <p className="text-slate-500 mb-4">
              Commencez par ajouter votre premier outil interactif
            </p>
            <Button 
              onClick={() => openToolDialog()}
              className="bg-slate-800 hover:bg-slate-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              Ajouter un outil
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredTools.map((tool) => (
              <Card key={tool.id} className="group bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden">
                {tool.preview_image && (
                  <div className="aspect-video overflow-hidden">
                    <img
                      src={tool.preview_image}
                      alt={tool.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                )}
                
                <div className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-slate-800 group-hover:text-slate-900 transition-colors line-clamp-1">
                      {tool.title}
                    </h3>
                    <Badge variant="secondary" className="ml-2 flex items-center space-x-1">
                      {getCategoryIcon(tool.category)}
                      <span className="text-xs">{tool.category}</span>
                    </Badge>
                  </div>
                  
                  <p className="text-sm text-slate-600 mb-4 line-clamp-2">
                    {tool.description}
                  </p>
                  
                  <div className="flex justify-between items-center">
                    <div className="flex space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setViewingTool(tool)}
                        className="border-slate-300 hover:bg-slate-100"
                      >
                        <Eye className="w-3 h-3 mr-1" />
                        Voir
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => openToolDialog(tool)}
                        className="border-slate-300 hover:bg-slate-100"
                      >
                        <Edit className="w-3 h-3 mr-1" />
                        Modifier
                      </Button>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDeleteTool(tool.id)}
                      className="border-red-300 text-red-600 hover:bg-red-50"
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>

      {/* Tool Viewer Dialog */}
      {viewingTool && (
        <Dialog open={!!viewingTool} onOpenChange={() => setViewingTool(null)}>
          <DialogContent className="max-w-6xl max-h-[90vh] overflow-hidden">
            <DialogHeader>
              <DialogTitle className="flex items-center space-x-2">
                {getCategoryIcon(viewingTool.category)}
                <span>{viewingTool.title}</span>
                <Badge variant="secondary">{viewingTool.category}</Badge>
              </DialogTitle>
            </DialogHeader>
            <div className="mt-4 h-[70vh] overflow-auto border rounded-lg">
              <iframe
                srcDoc={viewingTool.html_content}
                className="w-full h-full border-0"
                title={viewingTool.title}
                sandbox="allow-scripts allow-same-origin allow-forms"
              />
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}

export default App;