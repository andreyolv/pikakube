
graph TD
    subgraph Supply_Chain [Supply Chain Security]
        subgraph SAST_Tools [SAST]
            Dependabot[Dependabot]
            Bandit[Bandit]
            Gitleaks[Gitleaks]
        end

        subgraph Image_Security [Image]
            Trivy[Trivy]
            SBOM[SBOM]
            Cosign[Cosign]
            Container_Registry_Proxy[Image Container Registry Proxy]
        end
    end

    subgraph Admission_Policies [Admission and Policies]
        Kyverno[Kyverno]
        Kubescape[Kubescape]
    end

    subgraph AWS_Cloud [AWS]
        Prowler[Prowler]
        Cloud_Vulnerabilities[Cloud Vulnerabilities]
    end

    subgraph Runtime_Infrastructure [Runtime and Infrastructure]
        Tetragon[Tetragon]
        
        subgraph Auth_Block [Auth]
            SSO[SSO]
            Workload_Identity[Workload Identity]
        end
        
        subgraph Secrets_Management [Secrets]
            Hashicorp_Vault[Hashicorp Vault]
            External_Secrets[External Secrets]
        end
    end

    %% Supply Chain & Image Flow
    SAST_Tools --> Trivy
    Trivy --> SBOM
    SBOM --> Cosign
    Cosign --> Container_Registry_Proxy

    %% Admission Flow
    Container_Registry_Proxy --> Kyverno
    Kubescape --> Kyverno

    %% AWS & Runtime Flow
    Prowler --> Cloud_Vulnerabilities
    Cloud_Vulnerabilities --> Runtime_Infrastructure
    
    Hashicorp_Vault --> External_Secrets
    External_Secrets --> Workload_Identity
    SSO --> Workload_Identity
    Workload_Identity --> Tetragon
    
    %% Cross-block linkage
    Workload_Identity -.-> AWS_Cloud

