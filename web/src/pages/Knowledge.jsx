import { FolderOutlined } from '@ant-design/icons';
import { Button, Empty, Select, Spin } from 'antd';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import KnowledgePanel from '../components/KnowledgePanel';
import PageHeader from '../components/PageHeader';
import { getProjects } from '../services/api';

export default function Knowledge() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [projects, setProjects] = useState(null);
  const [loadError, setLoadError] = useState(false);

  const loadProjects = useCallback(async () => {
    setProjects(null);
    setLoadError(false);
    try {
      setProjects(await getProjects());
    } catch {
      setProjects([]);
      setLoadError(true);
    }
  }, []);

  useEffect(() => { loadProjects(); }, [loadProjects]);

  const projectId = useMemo(() => {
    const fromUrl = Number(searchParams.get('project'));
    if (fromUrl && projects?.some((p) => p.id === fromUrl)) return fromUrl;
    return projects?.[0]?.id ?? null;
  }, [searchParams, projects]);

  const handleSelect = (value) => {
    setSearchParams({ project: String(value) }, { replace: true });
  };

  if (projects === null) {
    return <div style={{ textAlign: 'center', padding: 80 }}><Spin /></div>;
  }

  if (loadError) {
    return (
      <div>
        <PageHeader title="知识库" description="加载项目列表后管理项目知识文档" />
        <Empty description="项目列表加载失败，请重试">
          <Button type="primary" onClick={loadProjects}>重新加载</Button>
        </Empty>
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        title="知识库"
        description="为每个项目沉淀业务规则、接口文档、缺陷记录。开启「知识库检索」后，AI 生成用例前会检索相关知识注入提示词。"
        extra={projects.length > 0 && (
          <div className="knowledge-project-switcher">
            <span className="knowledge-project-label">
              <FolderOutlined /> 当前项目
            </span>
            <Select
              className="knowledge-project-select"
              style={{ width: 220 }}
              value={projectId}
              onChange={handleSelect}
              options={projects.map((p) => ({ value: p.id, label: p.name }))}
              placeholder="选择项目"
            />
          </div>
        )}
      />

      {projects.length === 0 ? (
        <Empty description={<span>暂无项目，请先到 <Link to="/">全部项目</Link> 创建</span>} style={{ marginTop: 80 }} />
      ) : (
        <KnowledgePanel key={projectId} projectId={projectId} />
      )}
    </div>
  );
}
