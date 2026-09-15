import { lazy, Suspense } from 'react';
import { Spin } from 'antd';
import { BrowserRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import { getAuth } from './services/api';

const Evaluation = lazy(() => import('./pages/Evaluation'));
const GenerateFlow = lazy(() => import('./pages/GenerateFlow'));
const Knowledge = lazy(() => import('./pages/Knowledge'));
const Login = lazy(() => import('./pages/Login'));
const ProjectDetail = lazy(() => import('./pages/ProjectDetail'));
const ProjectGenerations = lazy(() => import('./pages/ProjectGenerations'));
const ProjectKnowledge = lazy(() => import('./pages/ProjectKnowledge'));
const ProjectList = lazy(() => import('./pages/ProjectList'));
const ProjectTestcases = lazy(() => import('./pages/ProjectTestcases'));
const ProjectTestTasks = lazy(() => import('./pages/ProjectTestTasks'));
const Register = lazy(() => import('./pages/Register'));
const Settings = lazy(() => import('./pages/Settings'));
const TestCaseLibrary = lazy(() => import('./pages/TestCaseLibrary'));
const TestTaskDetail = lazy(() => import('./pages/TestTaskDetail'));

function RequireAuth({ children }) {
  const location = useLocation();
  if (!getAuth()?.token) {
    return <Navigate to="/login" state={{ from: location.pathname + location.search }} replace />;
  }
  return children;
}

export default function App() {
  const baseUrl = import.meta.env.BASE_URL || '/';
  const basename = baseUrl === '/' ? undefined : baseUrl.replace(/\/$/, '');

  return (
    <BrowserRouter basename={basename}>
      <Suspense fallback={<div style={{ display: 'grid', minHeight: '50vh', placeItems: 'center' }}><Spin size="large" /></div>}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<RequireAuth><AppLayout /></RequireAuth>}>
            <Route index element={<ProjectList />} />
            <Route path="settings" element={<Settings />} />
            <Route path="testcases" element={<TestCaseLibrary />} />
            <Route path="knowledge" element={<Knowledge />} />
            <Route path="evaluation" element={<Evaluation />} />
            <Route path="projects/:projectId" element={<ProjectDetail />} />
            <Route path="projects/:projectId/generate" element={<GenerateFlow />} />
            <Route path="projects/:projectId/testcases" element={<ProjectTestcases />} />
            <Route path="projects/:projectId/tasks" element={<ProjectTestTasks />} />
            <Route path="projects/:projectId/tasks/:taskId" element={<TestTaskDetail />} />
            <Route path="projects/:projectId/knowledge" element={<ProjectKnowledge />} />
            <Route path="projects/:projectId/generations" element={<ProjectGenerations />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
