'use client';

import { useState, useEffect } from 'react';
import { getApiUrl, setBackendUrl, clearBackendUrl, isUsingCustomBackend } from '@/lib/api';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsModal({ isOpen, onClose }: SettingsModalProps) {
  const [backendUrl, setUrl] = useState('');
  const [isCustom, setIsCustom] = useState(false);
  const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');

  useEffect(() => {
    setUrl(getApiUrl());
    setIsCustom(isUsingCustomBackend());
  }, [isOpen]);

  const handleTest = async () => {
    setTestStatus('testing');
    try {
      const response = await fetch(`${backendUrl}/`, {
        method: 'GET',
        mode: 'cors',
      });
      if (response.ok) {
        setTestStatus('success');
      } else {
        setTestStatus('error');
      }
    } catch {
      setTestStatus('error');
    }
  };

  const handleSave = () => {
    if (backendUrl && backendUrl !== 'http://127.0.0.1:8000') {
      setBackendUrl(backendUrl);
    } else {
      clearBackendUrl();
    }
    onClose();
    // Reload to apply changes
    window.location.reload();
  };

  const handleReset = () => {
    clearBackendUrl();
    setUrl('http://127.0.0.1:8000');
    setIsCustom(false);
    setTestStatus('idle');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-xl p-6 max-w-md w-full mx-4">
        <h2 className="text-xl font-bold mb-4">⚙️ Ustawienia połączenia</h2>
        
        <div className="mb-4">
          <label className="block text-sm text-gray-400 mb-2">
            URL backendu
          </label>
          <input
            type="text"
            value={backendUrl}
            onChange={(e) => {
              setUrl(e.target.value);
              setTestStatus('idle');
            }}
            placeholder="https://twoj-ngrok-url.ngrok.io"
            className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-green-500 focus:outline-none"
          />
          <p className="text-xs text-gray-500 mt-1">
            Wklej URL z ngrok (np. https://abc123.ngrok.io)
          </p>
        </div>

        {isCustom && (
          <div className="mb-4 p-3 bg-yellow-900/30 border border-yellow-600/50 rounded-lg">
            <p className="text-sm text-yellow-400">
              ⚠️ Używasz niestandardowego URL backendu
            </p>
          </div>
        )}

        <div className="flex gap-2 mb-4">
          <button
            onClick={handleTest}
            disabled={testStatus === 'testing'}
            className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
          >
            {testStatus === 'testing' ? '⏳ Testowanie...' : '🔍 Testuj połączenie'}
          </button>
        </div>

        {testStatus === 'success' && (
          <div className="mb-4 p-3 bg-green-900/30 border border-green-600/50 rounded-lg">
            <p className="text-sm text-green-400">✅ Połączenie działa!</p>
          </div>
        )}

        {testStatus === 'error' && (
          <div className="mb-4 p-3 bg-red-900/30 border border-red-600/50 rounded-lg">
            <p className="text-sm text-red-400">❌ Nie można połączyć się z backendem</p>
            <p className="text-xs text-red-300 mt-1">Sprawdź czy URL jest poprawny i backend działa</p>
          </div>
        )}

        <div className="flex gap-2">
          <button
            onClick={handleReset}
            className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg transition-colors"
          >
            🔄 Resetuj
          </button>
          <button
            onClick={onClose}
            className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg transition-colors"
          >
            Anuluj
          </button>
          <button
            onClick={handleSave}
            className="flex-1 bg-green-600 hover:bg-green-500 text-white py-2 px-4 rounded-lg transition-colors"
          >
            💾 Zapisz
          </button>
        </div>
      </div>
    </div>
  );
}
